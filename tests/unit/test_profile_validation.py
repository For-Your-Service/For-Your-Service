"""Unit tests for veteran profile validation"""
import pytest
from src.validation import validate_veteran_profile, ValidationError


def test_valid_profile():
    """Test that a complete valid profile passes validation"""
    profile = {
        'veteran_id': 'VET001',
        'name': 'John Doe',
        'military_branch': 'Army',
        'mos': '18F',
        'clearance_level': 'Secret',
        'years_service': 10,
        'target_location': 'Greenville, SC'
    }
    assert validate_veteran_profile(profile) == True


def test_missing_required_field():
    """Test that missing required fields raise ValidationError"""
    profile = {'name': 'John Doe'}
    with pytest.raises(ValidationError, match="Missing required field: military_branch"):
        validate_veteran_profile(profile)


def test_invalid_clearance_level():
    """Test that invalid clearance levels are rejected"""
    profile = {
        'veteran_id': 'VET002',
        'name': 'Jane Smith',
        'military_branch': 'Navy',
        'mos': 'IT',
        'clearance_level': 'InvalidLevel',
        'years_service': 8,
        'target_location': 'San Diego, CA'
    }
    with pytest.raises(ValidationError, match="Invalid clearance_level"):
        validate_veteran_profile(profile)


def test_negative_years_service():
    """Test that negative years of service are rejected"""
    profile = {
        'veteran_id': 'VET003',
        'name': 'Bob Johnson',
        'military_branch': 'Marines',
        'mos': '0311',
        'clearance_level': 'Secret',
        'years_service': -5,
        'target_location': 'Quantico, VA'
    }
    with pytest.raises(ValidationError, match="years_service must be positive"):
        validate_veteran_profile(profile)


def test_invalid_location_format():
    """Test that invalid location formats are rejected"""
    profile = {
        'veteran_id': 'VET004',
        'name': 'Alice Williams',
        'military_branch': 'Air Force',
        'mos': '1N4X1',
        'clearance_level': 'TS/SCI',
        'years_service': 12,
        'target_location': 'InvalidFormat'
    }
    with pytest.raises(ValidationError, match="location must be in format 'City, STATE'"):
        validate_veteran_profile(profile)
