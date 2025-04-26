import requests

class TwitterClient:
    """Client for posting tweets to Twitter"""
    
    def __init__(self, auth):
        """Initialize with Twitter authentication"""
        self.auth = auth
        self.url = "https://api.twitter.com/2/tweets"
    
    def post_tweet(self, text):
        """Post a tweet with the given text"""
        payload = {"text": text}
        
        try:
            response = requests.post(
                auth=self.auth.get_auth(),
                url=self.url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            print(f"Tweet posted successfully: {text[:30]}...")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error posting tweet: {e}")
            return False