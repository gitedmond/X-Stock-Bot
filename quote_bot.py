import requests
from requests_oauthlib import OAuth1
import schedule
import time
from datetime import datetime, time as dt_time

consumer_key = "YVADXLeSl8EKAXI9ftNHhe5Iq"
consumer_secret = "zKORM4KjoOTMp8LAA7C2gdbQXOVYSSkt24N8ij4vDnlwJW1thD"
access_token = "1255508939992633347-Ppb8aODuTnYvGMykUIsgXXqsE4aTwj"
access_token_secret = "ZGhIwtLhpuy9YNPQDoY9e9kIhvGjOBMIouqyEIWTdxiVF"

# Define the API endpoints and headers for Quote data
quote_url = "https://twelve-data1.p.rapidapi.com/quote"
quote_headers = {
    "X-RapidAPI-Key": "9fb6f526damsh553ade645d8306bp1f207ajsnd8d72d6fe3d1",
    "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
}

# Define the symbol and other query parameters
symbol = "SPY"
interval = "1day"


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

# Function to fetch and save quote data
def fetch_and_save_quote_data():
    try:

        quote_querystring = {
            "interval": interval,
            "symbol": symbol,
            "outputsize": "30",
            "format": "json"
        }

        quote_response = requests.get(quote_url, headers=quote_headers, params=quote_querystring)
        quote_data = quote_response.json()

        if 'open' in quote_data:
            open_value = quote_data['open']
            high_value = quote_data['high']
            low_value = quote_data['low']
            close_value = quote_data['close']
            datetime_value = quote_data['datetime']  

            # Open a text file for writing
            with open('quote_data.txt', 'w') as txt_file:
                txt_file.write(f"$SPY Quote for {datetime_value}: \n")
                
                # Write the dynamic data
                txt_file.write(f"Open: {open_value}\n")
                txt_file.write(f"High: {high_value}\n")
                txt_file.write(f"Low: {low_value}\n")
                txt_file.write(f"Close: {close_value}\n")
                txt_file.write(f"#spy, #stocks, #technicalindicator, #gcgdwatcher\n")    

            print("Quote data saved to 'quote_data.txt'.")
        else:
            print("No 'open' data found in the response.")

    except Exception as e:
        print("An error occurred while fetching quote data:", str(e))
        
# Function to tweet the opening price at 8:03 AM
def tweet_open_price(consumer_key, consumer_secret, access_token, access_token_secret):
    try:
        with open('quote_data.txt', 'r') as txt_file:
            lines = txt_file.readlines()
            if len(lines) > 1:
                open_line = lines[1]  # Assuming 'Open' is the second line
                # Extract the number from the 'open' line
                open_number = open_line.split(":")[1].strip()
                tweet_content = f"$SPY has opened at {open_number} today."
                post_tweet(tweet_content, consumer_key, consumer_secret, access_token, access_token_secret)
            else:
                print("No 'Open' data found in the file.")

    except Exception as e:
        print("An error occurred while tweeting the opening price:", str(e))

# Function to tweet the contents of quote_data.txt at 3:03 PM
def tweet_quote_data(consumer_key, consumer_secret, access_token, access_token_secret):
    try:
        with open('quote_data.txt', 'r') as txt_file:
            tweet_content = txt_file.read()

        post_tweet(tweet_content, consumer_key, consumer_secret, access_token, access_token_secret)
    except Exception as e:
        print("An error occurred while tweeting quote data:", str(e))


schedule.every().day.at("15:05").do(fetch_and_save_quote_data)
schedule.every().day.at("15:06").do(tweet_quote_data, consumer_key, consumer_secret, access_token, access_token_secret)
schedule.every().day.at("08:35").do(fetch_and_save_quote_data)
schedule.every().day.at("08:36").do(tweet_open_price, consumer_key, consumer_secret, access_token, access_token_secret)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
