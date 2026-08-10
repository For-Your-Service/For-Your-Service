# Adzuna API Setup Guide

## Overview

Adzuna provides:
- Real salary data (not estimates)
- Market intelligence
- Regional volume metrics

## Registration

1. Register at https://developer.adzuna.com/
2. Create new app
3. Copy App ID and App Key

## Authentication

URL parameters:
```python
params = {
    "app_id": "your-app-id",
    "app_key": "your-app-key"
}
```

## Rate Limits

- **FREE Tier**: 5000 calls/month
- No paid tier for US market

## Unique Features

- `salary_is_predicted` flag
- Mean/median salary by location
- Historical trends
- Job category taxonomy
