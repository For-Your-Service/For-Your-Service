"""
test_haversine_distance_accuracy.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import pytest
from app.app import haversine_distance_miles

def test_distance_accuracy():
    # Distance between Greenville SC (34.8526, -82.3940) and Atlanta GA (33.7490, -84.3880) is ~140 miles
    dist = haversine_distance_miles(34.8526, -82.3940, 33.7490, -84.3880)
    assert 130 <= dist <= 155
