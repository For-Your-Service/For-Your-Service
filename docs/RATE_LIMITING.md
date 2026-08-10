# Rate Limiting Strategy

## For Your Service - API Rate Limit Management

### Provider Rate Limits

| Provider | Requests/Minute | Requests/Day | Notes |
|----------|----------------|--------------|-------|
| Indeed | 100 | Unlimited | Burst tolerance: 120 |
| LinkedIn | 60 | 5,000 | OAuth token-based |
| Monster | 120 | 10,000 | Per API key |
| CareerBuilder | 100 | 20,000 | Enterprise tier |
| ZipRecruiter | 50 | 5,000 | Strict enforcement |
| USAJobs | 4 | 250 | Per hour, not per minute |
| Dice | 30 | 1,000 | Tech-focused |
| Glassdoor | 20 | 500 | Very restrictive |

### Implementation Strategy

#### 1. Token Bucket Algorithm
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, rate_per_minute):
        self.rate = rate_per_minute
        self.tokens = rate_per_minute
        self.updated_at = time.time()
        
    def allow_request(self):
        now = time.time()
        elapsed = now - self.updated_at
        self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / 60))
        self.updated_at = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

#### 2. Exponential Backoff
When rate-limited (429 status):
* Wait 1 second, retry
* Wait 2 seconds, retry
* Wait 4 seconds, retry
* Wait 8 seconds, retry
* Max: 60 seconds

#### 3. Request Queuing
* Priority queue: Veteran intake > job updates > analytics
* Batch similar requests (e.g., 50 jobs per API call when supported)
* Off-peak scheduling for bulk operations (2am-6am EST)

### Monitoring & Alerts

```python
# Log rate limit hits
if response.status_code == 429:
    print(f"⚠️ Rate limited by {provider}")
    print(f"Retry-After: {response.headers.get('Retry-After')} seconds")
    
    # Alert if repeated hits
    if rate_limit_count > 3:
        send_slack_alert(f"Repeated rate limits from {provider}")
```

### Best Practices

* **Respect Retry-After headers** - Don't guess, use provider guidance
* **Implement circuit breakers** - Stop requests if provider is down
* **Cache aggressively** - Job posts don't change every minute
* **Batch operations** - Combine requests when API supports it
* **Monitor trends** - Track request counts over time

---

**Owner:** 7 Eagle Group  
**Updated:** 2026-08-10
