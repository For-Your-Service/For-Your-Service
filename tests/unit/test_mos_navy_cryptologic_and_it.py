import pytest
from app.mos_data import lookup_mos

def test_navy_cyber_and_crypto():
    for rating in ["IT", "CWT", "CTR", "CTI", "CTM", "IS"]:
        res = lookup_mos(rating)
        assert res is not None
        assert res["branch"] == "Navy"
