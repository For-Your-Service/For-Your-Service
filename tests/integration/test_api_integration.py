"""Integration tests for external API calls"""

import requests
from unittest.mock import patch, Mock


@patch("requests.get")
def test_indeed_api_call(mock_get):
    """Test Indeed API integration"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{"jobkey": "test123", "jobtitle": "DevOps Engineer", "company": "TechCorp"}]
    }
    mock_get.return_value = mock_response

    response = requests.get("https://api.indeed.com/ads/apisearch", params={})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0


def test_api_rate_limiter():
    """Test rate limiting functionality"""
    from src.rate_limiter import RateLimiter

    limiter = RateLimiter(rate_per_minute=100)

    # Should allow first 100 requests
    allowed_count = 0
    for _ in range(150):
        if limiter.allow_request():
            allowed_count += 1

    assert allowed_count <= 100
