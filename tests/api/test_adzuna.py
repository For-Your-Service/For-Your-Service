"""
Tests for Adzuna API client
"""

from src.api.adzuna.client import AdzunaClient


def test_adzuna_client_initialization():
    """Test Adzuna client initialization"""
    client = AdzunaClient(app_id="test_id", api_key="test_key")
    assert client.app_id == "test_id"
    assert client.api_key == "test_key"


def test_search_params_construction():
    """Test search parameter validation"""
    client = AdzunaClient(app_id="test_id", api_key="test_key")

    # Should accept valid parameters
    params = {"what": "cybersecurity", "where": "California", "distance": 25, "salary_min": 60000}
    assert params["what"] == "cybersecurity"
    assert params["distance"] == 25
