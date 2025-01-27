# Twitter Stock Bot (GC/GD Watcher)



## Overview
The X Stock Bot, also known as the GC/GD Watcher, is a Python-based bot that monitors stock market trends and posts updates to Twitter. It provides information about two key technical indicators: the Golden Cross and the Golden Death Cross. These indicators are calculated based on the Simple Moving Averages (SMA) for a specific stock symbol, such as SPY (S&P 500 ETF).

## Features
- Monitors stock market trends for the specified stock symbol (e.g., SPY).
- Alerts and identifies Golden Cross and Golden Death Cross events by calculating intersections via sign change of two most recently appended elements in an array `diff` 
- Tweets real-time updates to an X account.

## Prerequisites
Before running the bot, you need to set up the following:
- Twitter Developer Account with API keys and access tokens.
- RapidAPI account with access to Twelve Data API.
- Python 3.x installed on your system.


The bot will run in the background, periodically checking for events and tweeting updates.

## Configuration
You can customize the bot's behavior by modifying the following parameters in the Python scripts:
- `symbol`: The stock symbol to monitor (e.g., SPY).
- `interval`: The time interval for SMA calculations.
- `time_period_50`: The time period for the 50-day SMA.
- `time_period_200`: The time period for the 200-day SMA.
- `start_time` and `end_time`: The time range for bot execution (time of market open and market close).
- Twitter API keys and access tokens.
- RapidAPI keys for accessing Twelve Data API.

## Contributing
If you'd like to contribute to this project, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- This bot uses the Twelve Data API to retrieve stock market data.
- Special thanks to the Python community for creating powerful libraries like `requests` and `schedule`.

## Disclaimer
This bot is for educational and informational purposes only. It should not be considered financial advice. Always conduct your own research before making investment decisions.
