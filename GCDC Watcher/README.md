# GCDC Watcher – Stock SMA Crossover Bot

A simple bot that monitors a stock symbol’s SMA(50) vs SMA(200) and posts to Twitter when a golden cross or death cross occurs. This version focuses on production-minded hygiene: robust HTTP handling, correct Twitter v2 auth, logging, and timezone-aware market hours.

## Setup

1. Python 3.11+
2. Create and populate `.env` from `.env.example`:

```
cp .env.example .env
```

Required variables:
- `STOCK_API_KEY` – RapidAPI key
- `STOCK_API_HOST` – RapidAPI host for the stock data provider
- `TWITTER_BEARER_TOKEN` – Twitter API v2 bearer token with tweet write scope
- `LOG_LEVEL` – optional, defaults to `INFO`

3. Install dependencies:

```
pip install -r requirements.txt
```

## Running

```
python main.py
```

Configuration like symbol, market hours, and intervals live in `config.py`.

## Notes

- Twitter posting uses API v2 bearer token. Ensure your app has necessary permissions.
- HTTP requests use timeouts and raise on non-2xx; logs will reflect failures.
- Market hours are evaluated in `America/New_York` timezone and only on weekdays.

