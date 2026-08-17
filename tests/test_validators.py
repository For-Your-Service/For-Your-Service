"""
Tests for input validators
"""

from src.utils.validators import validate_mos, validate_email, validate_onet_code


def test_validate_mos():
    """Test MOS code validation"""
    # Valid Army MOS
    assert validate_mos("25B") is True
    assert validate_mos("35F") is True
    assert validate_mos("18B") is True

    # Valid Marine MOS
    assert validate_mos("0621") is True

    # Invalid
    assert validate_mos("ABC") is False
    assert validate_mos("123") is False


def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@company.co.uk") is True

    # Invalid
    assert validate_email("invalid") is False
    assert validate_email("@example.com") is False


def test_validate_onet_code():
    """Test O*NET code validation"""
    assert validate_onet_code("15-1212.00") is True
    assert validate_onet_code("29-2041.00") is True

    # Invalid
    assert validate_onet_code("15-1212") is False
    assert validate_onet_code("invalid") is False
