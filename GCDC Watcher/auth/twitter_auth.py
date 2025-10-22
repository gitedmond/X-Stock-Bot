from typing import Optional

class TwitterAuth:
    """Holds Twitter API v2 Bearer token for requests"""

    def __init__(self, bearer_token: Optional[str] = None):
        self.bearer_token = bearer_token

    def get_bearer_token(self) -> Optional[str]:
        return self.bearer_token