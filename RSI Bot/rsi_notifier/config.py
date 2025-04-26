
"""
Configuration settings for the RSI Notifier application.
"""

# List of stock symbols to monitor
SYMBOLS = [
    "LLY", "UAL", "IBM", "UPS", "FDX", "DIS", "V", "MA", "SPY", "QQQ",
    "SOFI", "TSLA", "AAPL", "AMZN", "GOOGL", "MSFT", "NVDA", "CMG",
    "META", "NFLX", "UBER", "COST", "HD", "AMD"
]

# API configurations
API_HOST = "twelve-data1.p.rapidapi.com"
API_BASE_URL = f"https://{API_HOST}/rsi"

# RSI thresholds for categorization
RSI_OVERSOLD_THRESHOLD = 30
RSI_ALMOST_OVERSOLD_THRESHOLD = 33
RSI_ALMOST_OVERBOUGHT_THRESHOLD = 67
RSI_OVERBOUGHT_THRESHOLD = 70

# API rate limiting settings
BATCH_SIZE = 6
BATCH_DELAY_SECONDS = 60
SYMBOL_DELAY_SECONDS = 3

# Schedule times (24-hour format)
SCHEDULE_TIMES = ["08:30", "11:45", "15:00"]

# Twitter API settings
TWITTER_API_URL = "https://api.twitter.com/2/tweets"
TWEET_CHARACTER_LIMIT = 280