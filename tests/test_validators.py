"""
Tests for input validators
"""
import pytest
from src.utils.validators import validate_mos, validate_email, validate_onet_code


def test_validate_mos():
    """Test MOS code validation"""
    # Valid Army MOS
    assert validate_mos("25B") == True
    assert validate_mos("35F") == True
    assert validate_mos("18B") == True
    
    # Valid Marine MOS
    assert validate_mos("0621") == True
    
    # Invalid
    assert validate_mos("ABC") == False
    assert validate_mos("123") == False


def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com") == True
    assert validate_email("user.name@company.co.uk") == True
    
    # Invalid
    assert validate_email("invalid") == False
    assert validate_email("@example.com") == False


def test_validate_onet_code():
    """Test O*NET code validation"""
    assert validate_onet_code("15-1212.00") == True
    assert validate_onet_code("29-2041.00") == True
    
    # Invalid
    assert validate_onet_code("15-1212") == False
    assert validate_onet_code("invalid") == False
