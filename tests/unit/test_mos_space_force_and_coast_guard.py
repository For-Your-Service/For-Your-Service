import pytest
from app.mos_data import lookup_mos

def test_space_and_uscg():
    for spec in ["5C0X1", "5I0X1", "5S0X1", "IS", "MST"]:
        res = lookup_mos(spec)
        assert res is not None
