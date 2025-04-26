"""
Twitter API client for the RSI Notifier application.
"""
import logging
import os
import requests
from requests_oauthlib import OAuth1
from rsi_notifier.config import TWITTER_API_URL, TWEET_CHARACTER_LIMIT

class TwitterAPI:
    """Handles Twitter API interactions."""
    
    def __init__(self):
        """Initialize the Twitter API client with credentials."""
        self.consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self.consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.url = TWITTER_API_URL
        self.logger = logging.getLogger(__name__)

    def post_tweet(self, tweet_content):
        """
        Post a tweet to Twitter.
        
        Args:
            tweet_content (str): The content of the tweet to post.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        # Ensure tweet is within character limit
        if len(tweet_content) > TWEET_CHARACTER_LIMIT:
            tweet_content = tweet_content[:TWEET_CHARACTER_LIMIT]
            
        auth = OAuth1(
            self.consumer_key, 
            self.consumer_secret, 
            self.access_token, 
            self.access_token_secret
        )
        payload = {"text": tweet_content}

        try:
            self.logger.debug(f"Posting tweet: {tweet_content}")
            response = requests.post(
                auth=auth,
                url=self.url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            self.logger.info("Tweet posted successfully.")
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error while posting tweet: {e}")
            return False