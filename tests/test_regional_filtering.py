"""Unit tests for regional filtering logic"""
import pytest
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in miles"""
    R = 3959  # Earth radius in miles
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def test_greenville_msa_center():
    """Test Greenville MSA center coordinates"""
    greenville_lat = 34.8526
    greenville_lon = -82.3940
    
    assert 34 < greenville_lat < 35
    assert -83 < greenville_lon < -82

def test_radius_filtering():
    """Test 50-mile radius filtering"""
    greenville = (34.8526, -82.3940)
    
    # Anderson (within 50 miles)
    anderson = (34.5034, -82.6501)
    distance_anderson = haversine_distance(*greenville, *anderson)
    assert distance_anderson < 50
    
    # Charlotte (outside 50 miles)
    charlotte = (35.2271, -80.8431)
    distance_charlotte = haversine_distance(*greenville, *charlotte)
    assert distance_charlotte > 50

def test_excluded_cities():
    """Test exclusion of non-Greenville MSA cities"""
    excluded = ["Charleston", "Columbia", "Myrtle Beach"]
    
    job_location = "Charleston, SC"
    
    for city in excluded:
        if city in job_location:
            assert False, f"{city} should be filtered out"
