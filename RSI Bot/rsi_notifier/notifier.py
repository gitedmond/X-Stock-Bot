"""
Notification logic for the RSI Notifier application.
"""
import logging
import time
from datetime import datetime
from rsi_notifier.config import BATCH_SIZE, BATCH_DELAY_SECONDS, SYMBOL_DELAY_SECONDS

class RSINotifier:
    """Manages the RSI checking process and notification creation."""
    
    def __init__(self, symbols, rsi_checker, twitter_api):
        """
        Initialize the RSI notifier.
        
        Args:
            symbols (list): List of stock symbols to monitor.
            rsi_checker (RSIChecker): Instance of the RSI checker.
            twitter_api (TwitterAPI): Instance of the Twitter API client.
        """
        self.symbols = symbols
        self.rsi_checker = rsi_checker
        self.twitter_api = twitter_api
        self.logger = logging.getLogger(__name__)

    def is_weekday(self):
        """
        Check if today is a weekday.
        
        Returns:
            bool: True if today is a weekday, False otherwise.
        """
        return datetime.now().weekday() < 5

    def batch_check_rsi(self):
        """Check RSI for all symbols and tweet results."""
        if not self.is_weekday():
            self.logger.info("It's a weekend. Skipping batch_check_rsi.")
            return

        self.logger.info("Starting batch RSI check")
        
        # Initialize result containers
        categories = {
            "overbought": [],
            "oversold": [],
            "almost_overbought": [],
            "almost_oversold": []
        }
        
        # Process symbols in batches to avoid API rate limits
        for i in range(0, len(self.symbols), BATCH_SIZE):
            current_batch = self.symbols[i:i+BATCH_SIZE]
            self._process_symbol_batch(current_batch, categories)
            
            # Only add delay if there are more batches to process
            if i + BATCH_SIZE < len(self.symbols):
                self.logger.debug(f"Pausing for {BATCH_DELAY_SECONDS} seconds between batches")
                time.sleep(BATCH_DELAY_SECONDS)
        
        self._post_rsi_summary(categories)
    
    def _process_symbol_batch(self, symbols_batch, categories):
        """
        Process a batch of symbols for RSI checking.
        
        Args:
            symbols_batch (list): Batch of symbols to process.
            categories (dict): Dictionary to store categorized results.
        """
        for symbol in symbols_batch:
            self.logger.info(f"Checking RSI for {symbol}")
            rsi_value, rsi_status = self.rsi_checker.check_rsi(symbol)
            
            if rsi_status == "error":
                self.logger.warning(f"Skipping {symbol} due to RSI retrieval error.")
                continue
            
            if rsi_status in categories:
                symbol_with_rsi = f"{symbol} (RSI: {rsi_value:.2f})"
                categories[rsi_status].append(symbol_with_rsi)
            
            # Add delay between API calls to avoid rate limiting
            time.sleep(SYMBOL_DELAY_SECONDS)
    
    def _post_rsi_summary(self, categories):
        """
        Create and post RSI summary tweet.
        
        Args:
            categories (dict): Dictionary with categorized RSI results.
        """
        # Check if we have any significant RSI values to report
        if not any(categories.values()):
            self.logger.info("No significant RSI values found. Skipping tweet.")
            return
        
        timestamp = datetime.now().strftime("%m-%d at %I:%M %p")
        body = f"RSI Summary for ({timestamp}):\n\n"
        
        # Add each category to the tweet body if it has values
        category_labels = {
            "overbought": "Overbought Symbols",
            "oversold": "Oversold Symbols",
            "almost_overbought": "Almost Overbought Symbols",
            "almost_oversold": "Almost Oversold Symbols"
        }
        
        for category, label in category_labels.items():
            if categories[category]:
                body += f"{label}:\n" + "\n".join(categories[category]) + "\n\n"
        
        self.logger.info("Posting RSI summary tweet")
        self.twitter_api.post_tweet(body)