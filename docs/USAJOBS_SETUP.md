# USAJOBS API Setup Guide

## Registration

1. Go to https://developer.usajobs.gov/
2. Click "Request API Key"
3. Fill out the form:
   - Email: your-email@example.com
   - Description: "Veteran job matching platform"

## Authentication

USAJOBS requires TWO headers:
- `Authorization-Key`: Your API key
- `User-Agent`: Your email address

## Rate Limits

- **FREE Tier**: 1000 requests/day
- **No paid tier available**
- Reset: Daily at midnight UTC

## Best Practices

- Always include User-Agent header (required)
- Use `ResultsPerPage=500` for efficiency
- Filter by `LocationName` at API level
- Cache results for 24 hours

## Example Request

```python
headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": "whall4.wh@gmail.com",
    "Authorization-Key": "your-api-key"
}
```
