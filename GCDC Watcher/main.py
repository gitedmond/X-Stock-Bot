from datetime import time as dt_time
from zoneinfo import ZoneInfo
from auth.twitter_auth import TwitterAuth
from clients.stock_data_client import StockDataClient
from clients.twitter_client import TwitterClient
from bots.stock_bot import StockBot
import config
from dotenv import load_dotenv
import os
import logging

def main():
    load_dotenv()

    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    # Validate required env vars
    required = ["STOCK_API_KEY", "STOCK_API_HOST", "TWITTER_BEARER_TOKEN"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        missing_str = ", ".join(missing)
        raise RuntimeError(f"Missing required environment variables: {missing_str}")

    twitter_auth = TwitterAuth(os.getenv("TWITTER_BEARER_TOKEN"))
    
    stock_client = StockDataClient(
        api_key=os.getenv("STOCK_API_KEY"),
        api_host=os.getenv("STOCK_API_HOST")
    )
    twitter_client = TwitterClient(bearer_token=twitter_auth.get_bearer_token())
    
    market_hours = {
        'start': dt_time(config.MARKET_START_HOUR, config.MARKET_START_MINUTE, tzinfo=ZoneInfo("America/New_York")),
        'end': dt_time(config.MARKET_END_HOUR, config.MARKET_END_MINUTE, tzinfo=ZoneInfo("America/New_York"))
    }

    stock_bot = StockBot(
        stock_client=stock_client,
        twitter_client=twitter_client,
        symbol=config.SYMBOL,
        data_file=config.DATA_FILE,
        market_hours=market_hours
    )
    
    stock_bot.run(
        sma_check_interval=config.SMA_CHECK_INTERVAL
    )

if __name__ == "__main__":
    main()
