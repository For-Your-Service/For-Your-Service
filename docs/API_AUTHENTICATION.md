# API Authentication Guide

## For Your Service - Authentication Patterns

### Overview
This document outlines authentication strategies for veteran intake APIs across multiple job board providers.

### Supported Authentication Methods

#### 1. API Key Authentication
**Providers:** Indeed, Monster, CareerBuilder, ZipRecruiter

```python
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
```

#### 2. OAuth 2.0
**Providers:** LinkedIn, Glassdoor

```python
from requests_oauthlib import OAuth2Session

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
authorization_url, state = oauth.authorization_url(auth_url)
```

#### 3. Basic Authentication
**Providers:** USAJobs (requires email registration)

```python
import base64
auth_string = base64.b64encode(f'{username}:{password}'.encode()).decode()
headers = {'Authorization': f'Basic {auth_string}'}
```

### Security Best Practices

* **Never commit API keys** - Use environment variables or Databricks Secrets
* **Rotate keys quarterly** - Set calendar reminders
* **Use least-privilege scopes** - Request only necessary permissions
* **Monitor rate limits** - Track usage to avoid throttling
* **Log authentication failures** - Alert on repeated failures

### Key Rotation Procedure

1. Generate new API key in provider dashboard
2. Update Databricks Secret: `databricks secrets put-secret --scope veteran_intake --key {provider}_api_key`
3. Test new key in staging environment
4. Update production secret
5. Revoke old key after 24-hour overlap period

### Provider-Specific Notes

#### Indeed
* Rate limit: 100 requests/minute
* Key format: 32-character alphanumeric
* Expires: Never (manual rotation recommended)

#### LinkedIn
* OAuth token expires: 60 days
* Refresh token expires: 1 year
* Scopes required: `r_liteprofile`, `r_basicprofile`, `w_member_social`

#### USAJobs
* No API key required
* Email-based registration
* User-Agent header mandatory: `{email} (Purpose: veteran job matching)`
* Rate limit: 250 requests/hour

---

**Maintained by:** 7 Eagle Group  
**Last Updated:** 2026-08-10
