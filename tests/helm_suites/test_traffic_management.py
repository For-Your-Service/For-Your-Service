"""
Test suite verifying Istio Gateway, VirtualService, and Canary routing configurations.
"""
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ISTIO_DIR = REPO_ROOT / "deployment" / "kubernetes" / "istio"

def test_gateway_configuration():
    gw_file = ISTIO_DIR / "gateway.yaml"
    assert gw_file.exists()
    with open(gw_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data["kind"] == "Gateway"
    assert data["spec"]["servers"][0]["port"]["number"] == 80

def test_destination_rule_subsets():
    dr_file = ISTIO_DIR / "destination-rule.yaml"
    assert dr_file.exists()
    with open(dr_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data["kind"] == "DestinationRule"
    assert data["spec"]["trafficPolicy"]["tls"]["mode"] == "ISTIO_MUTUAL"
    subsets = [s["name"] for s in data["spec"]["subsets"]]
    assert "v1" in subsets
    assert "v2" in subsets

def test_canary_virtual_service():
    canary_file = ISTIO_DIR / "canary-virtualservice.yaml"
    assert canary_file.exists()
    with open(canary_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    routes = data["spec"]["http"][0]["route"]
    weights = {r["destination"]["subset"]: r["weight"] for r in routes}
    assert weights["v1"] == 90
    assert weights["v2"] == 10
