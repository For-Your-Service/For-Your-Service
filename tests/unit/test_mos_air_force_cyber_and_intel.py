"""
test_mos_air_force_cyber_and_intel.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import pytest
from app.mos_data import lookup_mos

def test_af_cyber():
    for afsc in ["1D7X1", "1B4X1", "3P0X1"]:
        res = lookup_mos(afsc)
        assert res is not None
        assert res["branch"] == "Air Force"
