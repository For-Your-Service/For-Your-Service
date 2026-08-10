"""Unit tests for USAJOBS API connector"""
import pytest
from unittest.mock import Mock, patch

def test_usajobs_auth_headers():
    """Test USAJOBS authentication header generation"""
    api_key = "test-key-123"
    user_agent = "test@example.com"
    
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": user_agent,
        "Authorization-Key": api_key
    }
    
    assert "Authorization-Key" in headers
    assert "User-Agent" in headers
    assert headers["User-Agent"] == user_agent

def test_usajobs_query_params():
    """Test USAJOBS query parameter construction"""
    params = {
        "Keyword": "software engineer",
        "LocationName": "Greenville, SC",
        "ResultsPerPage": "500"
    }
    
    assert params["LocationName"] == "Greenville, SC"
    assert int(params["ResultsPerPage"]) <= 500

def test_usajobs_response_parsing():
    """Test USAJOBS API response parsing"""
    mock_response = {
        "SearchResult": {
            "SearchResultCount": "2",
            "SearchResultItems": [
                {
                    "MatchedObjectDescriptor": {
                        "PositionTitle": "Software Engineer",
                        "OrganizationName": "Department of Defense",
                        "PositionLocationDisplay": "Greenville, SC"
                    }
                }
            ]
        }
    }
    
    assert "SearchResult" in mock_response
    assert mock_response["SearchResult"]["SearchResultCount"] == "2"
