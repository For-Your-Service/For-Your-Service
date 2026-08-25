"""
Test suite verifying Istio security policies and mTLS zero-trust configurations.
"""
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ISTIO_DIR = REPO_ROOT / "deployment" / "kubernetes" / "istio"

def test_peer_authentication_strict():
    pa_file = ISTIO_DIR / "peer-authentication.yaml"
    assert pa_file.exists()
    with open(pa_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data["spec"]["mtls"]["mode"] == "STRICT"

def test_authorization_policies_valid():
    policies_dir = ISTIO_DIR / "policies"
    if (policies_dir / "authorization-policy.yaml").exists():
        with open(policies_dir / "authorization-policy.yaml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data["kind"] == "AuthorizationPolicy"

def test_service_entries_exist():
    policies_dir = ISTIO_DIR / "policies"
    for se in ["service-entry-usajobs.yaml", "service-entry-jsearch.yaml", "service-entry-databricks.yaml"]:
        p = policies_dir / se
        assert p.exists(), f"Missing service entry {se}"
        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data["kind"] == "ServiceEntry"
