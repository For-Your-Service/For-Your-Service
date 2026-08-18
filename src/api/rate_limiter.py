"""
Rate Limiter for API Calls
"""

import time
from collections import deque


class RateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, max_calls: int = 60, time_window: int = 60, rate_per_minute: int = None):
        """
        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
            rate_per_minute: Shortcut to configure calls per minute
        """
        if rate_per_minute is not None:
            self.max_calls = rate_per_minute
            self.time_window = 60
        else:
            self.max_calls = max_calls
            self.time_window = time_window
        self.calls = deque()

    def allow_request(self) -> bool:
        """Check if request is allowed without blocking."""
        now = time.time()
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()

        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()

        # Remove old calls outside time window
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()

        # If at limit, wait
        if len(self.calls) >= self.max_calls:
            sleep_time = self.calls[0] + self.time_window - now
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.wait_if_needed()  # Recursive check

        # Record this call
        self.calls.append(now)


# Pre-configured rate limiters
class APIRateLimiters:
    """Rate limiters for each API"""

    # Adzuna: 1000 calls/month = ~33/day = ~1.4/hour
    adzuna = RateLimiter(max_calls=1, time_window=3600)  # 1 per hour (conservative)

    # BLS: 500 calls/day (registered)
    bls = RateLimiter(max_calls=20, time_window=3600)  # 20 per hour

    # USAJobs: Unlimited (reasonable use)
    usajobs = RateLimiter(max_calls=10, time_window=60)  # 10 per minute

    # O*NET: Unlimited
    onet = RateLimiter(max_calls=10, time_window=60)  # 10 per minute

    # CareerOneStop: Unlimited
    careeronestop = RateLimiter(max_calls=10, time_window=60)  # 10 per minute
