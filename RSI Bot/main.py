#!/usr/bin/env python3
"""
RSI Notifier - Main Entry Point
Monitors RSI values for configured stocks and posts alerts to Twitter.
"""
import logging
import os
from dotenv import load_dotenv

from rsi_notifier.twitter_api import TwitterAPI
from rsi_notifier.rsi_checker import RSIChecker
from rsi_notifier.notifier import RSINotifier
from rsi_notifier.scheduler import Scheduler
from rsi_notifier.config import SYMBOLS

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger = setup_logging()
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        logger.error("API_KEY environment variable not found. Check your .env file.")
        return 1
    
    # Initialize components
    logger.info("Initializing RSI Notifier components")
    twitter_api = TwitterAPI()
    rsi_checker = RSIChecker(api_key)
    rsi_notifier = RSINotifier(SYMBOLS, rsi_checker, twitter_api)
    
    # Start the scheduler
    logger.info("Starting the scheduler")
    scheduler = Scheduler(rsi_notifier)
    scheduler.start()
    
    return 0

if __name__ == "__main__":
    exit(main())