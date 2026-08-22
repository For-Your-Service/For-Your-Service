import pytest
from app.app import evaluate_clearance_match

def test_clearance_levels():
    assert evaluate_clearance_match("TS/SCI", "Secret") >= 1.0
    assert evaluate_clearance_match("Secret", "Secret") >= 1.0
    assert evaluate_clearance_match("None", "Secret") < 0.6
