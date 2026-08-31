"""
test_mos_marine_corps_recon_and_cyber.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import pytest
from app.mos_data import lookup_mos

def test_marine_mos():
    for mos in ["0311", "0671", "0689", "0431", "5811"]:
        res = lookup_mos(mos)
        assert res is not None
        assert res["branch"] == "Marine Corps"
