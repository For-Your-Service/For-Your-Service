"""
test_clearance_hierarchy_evaluator.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import pytest
from app.app import evaluate_clearance

def test_clearance_levels():
    eligible_higher, _, status1, _ = evaluate_clearance("TS/SCI", "Secret")
    assert eligible_higher is True
    assert status1 == "pass"

    eligible_equal, _, status2, _ = evaluate_clearance("Secret", "Secret")
    assert eligible_equal is True
    assert status2 == "pass"

    eligible_lower, _, status3, _ = evaluate_clearance("None / Unsure", "Secret")
    assert eligible_lower is False
    assert status3 == "fail"
