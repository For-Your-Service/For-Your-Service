import pytest
from app.app import calculate_haversine_distance

def test_distance_accuracy():
    # Distance between Greenville SC (34.8526, -82.3940) and Atlanta GA (33.7490, -84.3880) is ~140 miles
    dist = calculate_haversine_distance(34.8526, -82.3940, 33.7490, -84.3880)
    assert 130 <= dist <= 155
