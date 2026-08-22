import pytest
from app.mos_data import lookup_mos

def test_army_combat_arms():
    for mos in ["11B", "11C", "18F", "18Z", "12B", "15T"]:
        res = lookup_mos(mos)
        assert res is not None
        assert res["branch"] == "Army"
        assert len(res["transferable_skills"]) >= 2
