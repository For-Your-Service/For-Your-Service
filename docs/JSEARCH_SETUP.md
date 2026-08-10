# JSearch API Setup Guide

## Overview

JSearch aggregates jobs from:
- Indeed
- LinkedIn  
- Glassdoor
- ZipRecruiter

## Registration

1. Sign up at https://rapidapi.com/ (FREE)
2. Go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
3. Click "Subscribe to Test"
4. Select **FREE plan**: 1000 requests/month

## Authentication

RapidAPI gateway requires:
```python
headers = {
    "X-RapidAPI-Key": "your-rapidapi-key",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}
```

## Rate Limits

| Plan | Requests/Month | Cost |
|------|----------------|------|
| FREE | 1,000 | $0 |
| Basic | 5,000 | $9.99 |
| Pro | 25,000 | $29.99 |

## Query Parameters

- `query`: Natural language search
- `date_posted`: Filter freshness
- `radius`: Miles from location
- `employment_types`: FULLTIME,CONTRACTOR
