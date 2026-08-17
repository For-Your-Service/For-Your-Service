"""
Common API Error Handling
"""

import time
import requests
from typing import Callable, Any
from functools import wraps


class APIError(Exception):
    """Base API error"""


class RateLimitError(APIError):
    """Rate limit exceeded"""


class AuthenticationError(APIError):
    """Authentication failed"""


def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 2.0):
    """Decorator for retrying API calls with exponential backoff"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise APIError(f"Max retries exceeded: {str(e)}")

                    # Check for rate limit
                    if hasattr(e, "response") and e.response.status_code == 429:
                        raise RateLimitError("Rate limit exceeded")

                    # Check for auth errors
                    if hasattr(e, "response") and e.response.status_code in [401, 403]:
                        raise AuthenticationError("Authentication failed")

                    # Exponential backoff
                    wait_time = backoff_factor**attempt
                    time.sleep(wait_time)

            raise APIError("Unexpected error in retry logic")

        return wrapper

    return decorator


def handle_api_response(response: requests.Response) -> dict:
    """Handle API response with error checking"""
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")
    elif response.status_code in [401, 403]:
        raise AuthenticationError("Invalid credentials")
    elif response.status_code == 404:
        raise APIError("Resource not found")
    else:
        raise APIError(f"API error: {response.status_code} - {response.text}")
