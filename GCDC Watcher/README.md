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

## How Alerts Work

- Data fetch:
  - The bot requests SMA(50) and SMA(200) values for the configured `SYMBOL` from the stock data API at a fixed interval (`SMA_CHECK_INTERVAL` minutes).
- Difference tracking:
  - It computes `diff = SMA50 - SMA200` and appends it to an in-memory list of recent differences.
- Crossover detection:
  - When at least two differences exist, a sign change between the last two values signals an intersection (crossover).
  - Negative → non-negative: Golden Cross (bullish) alert.
  - Positive → non-positive: Death Cross (bearish) alert.
- Market-time guardrails:
  - Checks only run and trigger during market hours on weekdays, evaluated in `America/New_York` timezone.
- Notifications:
  - On detection, the bot logs the event and posts a tweet via Twitter API v2. Failures are logged; the bot continues running.

Note: The list of differences is kept in memory only; restarting the bot resets this history and may affect whether an immediate alert fires after a restart.
