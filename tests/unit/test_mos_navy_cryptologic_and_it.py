"""
test_mos_navy_cryptologic_and_it.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import pytest
from app.mos_data import lookup_mos

def test_navy_cyber_and_crypto():
    for rating in ["IT", "CTN", "IS", "ET", "MA"]:
        res = lookup_mos(rating)
        assert res is not None
        assert res["branch"] == "Navy"
