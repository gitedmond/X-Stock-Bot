"""
RSI calculation and categorization for the RSI Notifier application.
"""
import logging
import requests
from rsi_notifier.config import (
    API_BASE_URL, API_HOST,
    RSI_OVERSOLD_THRESHOLD, RSI_ALMOST_OVERSOLD_THRESHOLD,
    RSI_ALMOST_OVERBOUGHT_THRESHOLD, RSI_OVERBOUGHT_THRESHOLD
)

class RSIChecker:
    """Retrieves and categorizes RSI values for stock symbols."""
    
    def __init__(self, api_key):
        """
        Initialize the RSI checker.
        
        Args:
            api_key (str): The API key for the RSI data provider.
        """
        self.api_key = api_key
        self.url = API_BASE_URL
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": API_HOST
        }
        self.logger = logging.getLogger(__name__)

    def check_rsi(self, symbol):
        """
        Check RSI value for a given symbol.
        
        Args:
            symbol (str): The stock symbol to check.
            
        Returns:
            tuple: (rsi_value, status) where rsi_value is a float or None,
                  and status is a string categorizing the RSI value.
        """
        querystring = {
            "format": "json",
            "time_period": "14",
            "interval": "1day",
            "series_type": "close",
            "outputsize": "1",
            "symbol": symbol
        }
        
        try:
            self.logger.debug(f"Requesting RSI data for {symbol}")
            response = requests.get(self.url, headers=self.headers, params=querystring)
            response.raise_for_status()
            data = response.json()

            if 'values' in data and len(data['values']) > 0:
                rsi_value = float(data['values'][0]['rsi'])
                status = self._categorize_rsi(rsi_value, symbol)
                return rsi_value, status
            else:
                self.logger.warning(f"No RSI values found in response for {symbol}")
        
        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            self.logger.error(f"Error retrieving RSI for {symbol}: {e}")
        
        self.logger.warning(f"No RSI data available for {symbol}")
        return None, "error"
    
    def _categorize_rsi(self, rsi_value, symbol):
        """
        Categorize RSI value and log accordingly.
        
        Args:
            rsi_value (float): The RSI value to categorize.
            symbol (str): The stock symbol (for logging).
            
        Returns:
            str: The category of the RSI value.
        """
        if rsi_value <= RSI_OVERSOLD_THRESHOLD:
            self.logger.info(f"{symbol} is Oversold! (RSI: {rsi_value:.2f})")
            return "oversold"
        elif rsi_value >= RSI_OVERBOUGHT_THRESHOLD:
            self.logger.info(f"{symbol} is Overbought! (RSI: {rsi_value:.2f})")
            return "overbought"
        elif rsi_value <= RSI_ALMOST_OVERSOLD_THRESHOLD:
            self.logger.info(f"{symbol} is Almost Oversold (RSI: {rsi_value:.2f})")
            return "almost_oversold"
        elif rsi_value >= RSI_ALMOST_OVERBOUGHT_THRESHOLD:
            self.logger.info(f"{symbol} is Almost Overbought (RSI: {rsi_value:.2f})")
            return "almost_overbought"
        else:
            self.logger.debug(f"{symbol} is Neutral (RSI: {rsi_value:.2f})")
            return "neutral"