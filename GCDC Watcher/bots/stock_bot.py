from typing import List, Dict, Any
import schedule
import time
from datetime import datetime, time as dt_time
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)

class StockBot:
    """Bot that monitors stock data and posts tweets about significant events"""
    
    def __init__(self, stock_client, twitter_client, symbol, data_file, market_hours=None):
        """Initialize with necessary clients and configuration"""
        self.stock_client = stock_client
        self.twitter_client = twitter_client
        self.symbol = symbol
        self.sma_differences: List[float] = []
        self.data_file = data_file
        
        if market_hours is None:
            self.market_hours = {
                'start': dt_time(8, 30, tzinfo=ZoneInfo("America/New_York")),
                'end': dt_time(15, 0, tzinfo=ZoneInfo("America/New_York"))
            }
        else:
            self.market_hours = market_hours
    
    def is_market_hours(self):
        """Check if current time is during market hours and it's a weekday"""
        now = datetime.now(tz=ZoneInfo("America/New_York"))
        current_time = now.timetz()
        current_day = now.weekday()
        return (self.market_hours['start'] <= current_time <= self.market_hours['end'] 
                and current_day < 5)  # 0-4 is Monday-Friday
    
    def is_weekday(self):
        """Check if current day is a weekday"""
        return datetime.now(tz=ZoneInfo("America/New_York")).weekday() < 5

    def check_sma_crossover(self):
        """Check for SMA crossover events (Golden Cross/Death Cross)"""
        if not self.is_market_hours():
            return
        
        try:
            sma50_data = self.stock_client.get_sma(self.symbol, "50")
            sma50 = float(sma50_data["values"][0]["sma"])
            
            sma200_data = self.stock_client.get_sma(self.symbol, "200")
            sma200 = float(sma200_data["values"][0]["sma"])
            
            difference = round(sma50 - sma200, 5)
            self.sma_differences.append(difference)
            
            logger.info("SMA50: %s | SMA200: %s | Difference: %s", sma50, sma200, difference)
            
            if len(self.sma_differences) >= 2:
                prev_diff = self.sma_differences[-2]
                current_diff = self.sma_differences[-1]
                
                if prev_diff < 0 and current_diff >= 0:
                    message = (f"${self.symbol} has experienced a Golden Cross! "
                              f"The 50-day SMA has crossed above the 200-day SMA, "
                              f"potentially indicating a bullish trend.")
                    self.twitter_client.post_tweet(message)
                    logger.info("Golden Cross detected!")
                
                elif prev_diff > 0 and current_diff <= 0:
                    message = (f"${self.symbol} has experienced a Golden Death! "
                              f"The 50-day SMA has crossed below the 200-day SMA, "
                              f"potentially indicating a bearish trend.")
                    self.twitter_client.post_tweet(message)
                    logger.info("Golden Death detected!")
                    
            if len(self.sma_differences) > 100:
                self.sma_differences = self.sma_differences[-50:]
                
        except Exception as e:
            logger.error("Error checking SMA crossover: %s", e)
    
    def schedule_tasks(self, sma_check_interval: int):
        """Schedule all routine tasks"""
        schedule.every(sma_check_interval).minutes.do(self.check_sma_crossover)
    
    def run(self, sma_check_interval: int):
        """Run the bot"""
        self.schedule_tasks(sma_check_interval)
        
        logger.info("Stock Bot started for %s. Monitoring for events...", self.symbol)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped manually.")
