"""
Tests for O*NET API client
"""

from src.api.onet.client import ONetClient


def test_onet_client_initialization():
    """Test O*NET client initialization"""
    client = ONetClient(username="test@example.com")
    assert client.username == "test@example.com"
    assert client.BASE_URL == "https://services.onetcenter.org/ws/online"


def test_occupation_code_format():
    """Test O*NET occupation code format"""
    # Valid format: XX-XXXX.XX
    valid_code = "15-1212.00"
    assert len(valid_code.split("-")) == 2
    assert len(valid_code.split(".")) == 2
