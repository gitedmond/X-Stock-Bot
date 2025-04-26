from requests_oauthlib import OAuth1

class TwitterAuth:
    """Handles authentication for Twitter API"""
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """Initialize with Twitter API credentials"""
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
    def get_auth(self):
        """Return OAuth1 authentication object for Twitter API requests"""
        return OAuth1(
            self.consumer_key, 
            self.consumer_secret, 
            self.access_token, 
            self.access_token_secret
        )