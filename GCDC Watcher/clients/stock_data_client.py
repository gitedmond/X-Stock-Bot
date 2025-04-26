import requests

class StockDataClient:
    """Client for fetching stock data from API"""
    
    def __init__(self, api_key, api_host):
        """Initialize with API credentials"""
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }
        self.base_url = f"https://{api_host}"
    
    def get_quote(self, symbol, interval="1day", outputsize="30"):
        """Get current quote data for a stock symbol"""
        url = f"{self.base_url}/quote"
        querystring = {
            "interval": interval,
            "symbol": symbol,
            "outputsize": outputsize,
            "format": "json"
        }
        
        response = requests.get(url, headers=self.headers, params=querystring)
        return response.json()
    
    def get_sma(self, symbol, time_period, interval="1min", outputsize="1"):
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
        
        response = requests.get(url, headers=self.headers, params=querystring)
        return response.json()