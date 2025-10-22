from typing import Optional
import requests
import logging

logger = logging.getLogger(__name__)

class TwitterClient:
    """Client for posting tweets to Twitter"""
    
    def __init__(self, bearer_token: Optional[str] = None):
        """Initialize with Bearer token for Twitter API v2"""
        self.bearer_token = bearer_token
        self.url = "https://api.twitter.com/2/tweets"
    
    def post_tweet(self, text: str) -> bool:
        """Post a tweet with the given text"""
        if not self.bearer_token:
            logger.error("Missing Twitter Bearer token")
            return False

        payload = {"text": text}
        
        try:
            response = requests.post(
                url=self.url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.bearer_token}",
                },
                timeout=15,
            )
            response.raise_for_status()
            logger.info("Tweet posted successfully: %s", text[:60])
            return True
        except requests.exceptions.RequestException as e:
            logger.error("Error posting tweet: %s", e)
            return False
