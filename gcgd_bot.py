import requests
from requests_oauthlib import OAuth1
import schedule
import time
from datetime import datetime, time as dt_time

consumer_key = "YVADXLeSl8EKAXI9ftNHhe5Iq"
consumer_secret = "zKORM4KjoOTMp8LAA7C2gdbQXOVYSSkt24N8ij4vDnlwJW1thD"
access_token = "1255508939992633347-Ppb8aODuTnYvGMykUIsgXXqsE4aTwj"
access_token_secret = "ZGhIwtLhpuy9YNPQDoY9e9kIhvGjOBMIouqyEIWTdxiVF"

# Define the API endpoints and headers for SMA data
sma_url = "https://twelve-data1.p.rapidapi.com/sma"
sma_headers = {
    "X-RapidAPI-Key": "9fb6f526damsh553ade645d8306bp1f207ajsnd8d72d6fe3d1",
    "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
}

# Define the symbol and other query parameters
symbol = "SPY"
interval = "5min"
time_period_50 = "50"
time_period_200 = "200"

# Define the start and end times for running the loop
start_time = dt_time(8, 30)
end_time = dt_time(15, 0)

# Function to post a tweet
def post_tweet(tweet_content, consumer_key, consumer_secret, access_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    payload = {"text": tweet_content}

    try:
        request = requests.post(
            auth=auth,
            url=url,
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        request.raise_for_status()
        print("Tweet posted successfully.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Function to check for Golden Cross or Golden Death and post tweets
def check_and_tweet():
    current_time = datetime.now().time()

    # Check if the current time is within the specified range (8:30 AM to 3:00 PM)
    if start_time <= current_time <= end_time:
        # Request SMA for 50-time period and 200-time period
        querystring50 = {
            "interval": interval,
            "symbol": symbol,
            "time_period": time_period_50,
            "outputsize": "3",
            "format": "json",
            "series_type": "close"
        }

        response50 = requests.get(sma_url, headers=sma_headers, params=querystring50)
        data50 = response50.json()

        # Request SMA for 200-time period
        querystring200 = {
            "interval": interval,
            "symbol": symbol,
            "time_period": time_period_200,
            "outputsize": "3",
            "format": "json",
            "series_type": "close"
        }

        response200 = requests.get(sma_url, headers=sma_headers, params=querystring200)
        data200 = response200.json()

        # Check if the requests were successful
        if data50['status'] == 'ok' and data200['status'] == 'ok':
            # Access the list of values for both 50-day and 200-day SMAs
            sma_values_50 = data50['values']
            sma_values_200 = data200['values']

            # Check if there are at least two entries in the lists
            if len(sma_values_50) >= 2 and len(sma_values_200) >= 2:
                # Get the most recent and previous SMA values
                latest_sma_50 = float(sma_values_50[0]['sma'])
                previous_sma_50 = float(sma_values_50[2]['sma'])

                latest_sma_200 = float(sma_values_200[0]['sma'])
                previous_sma_200 = float(sma_values_200[2]['sma'])

                # Check for Golden Cross or Golden Death
                if latest_sma_50 > latest_sma_200 and previous_sma_50 <= previous_sma_200:
                    post_tweet("$SPY has experienced a Golden Cross.", consumer_key, consumer_secret, access_token, access_token_secret)
                elif latest_sma_50 < latest_sma_200 and previous_sma_50 >= previous_sma_200:
                    post_tweet("$SPY has experienced a Golden Death.", consumer_key, consumer_secret, access_token, access_token_secret)
            else:
                print("Insufficient data for comparison (less than 2 entries for one or both SMAs).")
        else:
            print("Error: Unable to retrieve SMA data")

# Schedule the SMA data retrieval task every minute
schedule.every(1).minutes.do(check_and_tweet)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)


