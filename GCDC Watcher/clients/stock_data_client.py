from typing import Any, Dict
import requests
import logging

logger = logging.getLogger(__name__)

class StockDataClient:
    """Client for fetching stock data from API"""
    
    def __init__(self, api_key: str, api_host: str):
        """Initialize with API credentials"""
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }
        self.base_url = f"https://{api_host}"
    
    def get_quote(self, symbol: str, interval: str = "1day", outputsize: str = "30") -> Dict[str, Any]:
        """Get current quote data for a stock symbol"""
        url = f"{self.base_url}/quote"
        querystring = {
            "interval": interval,
            "symbol": symbol,
            "outputsize": outputsize,
            "format": "json"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=querystring, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("Unexpected response format for quote")
            return data
        except (requests.RequestException, ValueError) as e:
            logger.error("Quote request failed for %s: %s", symbol, e)
            raise
    
    def get_sma(self, symbol: str, time_period: str, interval: str = "1min", outputsize: str = "1") -> Dict[str, Any]:
        """Get Simple Moving Average (SMA) for a stock symbol"""
        url = f"{self.base_url}/sma"
        querystring = {
            "symbol": symbol,
            "time_period": time_period,
            "interval": interval,
            "outputsize": outputsize,
            "format": "json",
            "series_type": "close"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=querystring, timeout=15)
            response.raise_for_status()
            data = response.json()
            # Basic schema check
            if not isinstance(data, dict) or "values" not in data or not data["values"]:
                raise ValueError("SMA response missing 'values'")
            return data
        except (requests.RequestException, ValueError) as e:
            logger.error("SMA request failed for %s (period=%s): %s", symbol, time_period, e)
            raise
