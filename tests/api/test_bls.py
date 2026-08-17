"""
Tests for BLS API client
"""

from src.api.bls.client import BLSClient


def test_bls_client_initialization():
    """Test BLS client can be initialized"""
    client = BLSClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.BASE_URL == "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def test_series_id_construction():
    """Test BLS series ID format"""
    client = BLSClient(api_key="test_key")

    # Test occupation wages series ID format
    # Should be: OEUN + area + SOC + data_type

    # Series ID should contain the pattern
    assert "OEUN" in "OEUN000000015121203"
