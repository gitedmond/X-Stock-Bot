from datetime import time as dt_time
from auth.twitter_auth import TwitterAuth
from clients.stock_data_client import StockDataClient
from clients.twitter_client import TwitterClient
from bots.stock_bot import StockBot
import config
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    # Create Twitter auth
    twitter_auth = TwitterAuth(
        os.getenv("TWITTER_CONSUMER_KEY"),
        os.getenv("TWITTER_CONSUMER_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )
    
    # Create API clients
    stock_client = StockDataClient(
        api_key=os.getenv("STOCK_API_KEY"),
        api_host=os.getenv("STOCK_API_HOST")
    )
    twitter_client = TwitterClient(twitter_auth)
    
    # Set market hours
    market_hours = {
        'start': dt_time(config.MARKET_START_HOUR, config.MARKET_START_MINUTE),
        'end': dt_time(config.MARKET_END_HOUR, config.MARKET_END_MINUTE)
    }
    
    # Create and run the Stock Bot
    stock_bot = StockBot(
        stock_client=stock_client,
        twitter_client=twitter_client,
        symbol=config.SYMBOL,
        data_file=config.DATA_FILE,
        market_hours=market_hours
    )
    
    # Run the bot with schedule parameters from config
    stock_bot.run(
        sma_check_interval=config.SMA_CHECK_INTERVAL
    )

if __name__ == "__main__":
    main()