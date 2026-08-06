"""
Tests for USAJobs API client
"""
import pytest
from src.api.usajobs.client import USAJobsClient


def test_usajobs_client_initialization():
    """Test USAJobs client can be initialized"""
    client = USAJobsClient(api_key="test_key", user_agent="test@example.com")
    assert client.api_key == "test_key"
    assert client.user_agent == "test@example.com"


def test_build_search_params():
    """Test search parameter construction"""
    client = USAJobsClient(api_key="test_key", user_agent="test@example.com")
    params = client._build_search_params(
        keyword="cybersecurity",
        location="California"
    )
    assert params["Keyword"] == "cybersecurity"
    assert params["LocationName"] == "California"
    assert params["ResultsPerPage"] == 100
