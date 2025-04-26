# Configuration settings for the stock bot

# Stock symbol to monitor
SYMBOL = "SPY"

# File to store stock data
DATA_FILE = "data/data.txt"

# Market hours (Eastern Time)
MARKET_START_HOUR = 8
MARKET_START_MINUTE = 30
MARKET_END_HOUR = 15
MARKET_END_MINUTE = 0

# Schedule times
MORNING_FETCH_TIME = "08:35"
MORNING_TWEET_TIME = "08:36"
EVENING_FETCH_TIME = "15:05"
EVENING_TWEET_TIME = "15:06"

# SMA crossover check interval (minutes)
SMA_CHECK_INTERVAL = 1