import pytest
from app.mos_data import lookup_mos

def test_army_combat_arms():
    for mos in ["11B", "11C", "11A", "18B", "18C", "18D", "18E", "18F", "18Z"]:
        res = lookup_mos(mos)
        assert res is not None
        assert res["branch"] == "Army"
        assert len(res["skills"]) >= 2
