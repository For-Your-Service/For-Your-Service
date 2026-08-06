"""
Tests for CareerOneStop API client
"""
import pytest
from src.api.careeronestop.client import CareerOneStopClient


def test_careeronestop_client_initialization():
    """Test CareerOneStop client initialization"""
    client = CareerOneStopClient(
        user_id="test_user",
        authorization_token="test_token"
    )
    assert client.user_id == "test_user"
    assert client.BASE_URL == "https://api.careeronestop.org/v1"
