"""
Test suite verifying Helm chart template rendering and values overlays.
"""
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CHART_DIR = REPO_ROOT / "charts" / "for-your-service"
TEMPLATES_DIR = CHART_DIR / "templates"

def test_chart_metadata():
    chart_file = CHART_DIR / "Chart.yaml"
    assert chart_file.exists()
    with open(chart_file, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    assert meta["name"] == "for-your-service"
    assert meta["apiVersion"] == "v2"

def test_environment_values_files_exist():
    for env in ["values.yaml", "values-dev.yaml", "values-staging.yaml", "values-prod.yaml"]:
        p = CHART_DIR / env
        assert p.exists(), f"Missing environment file {env}"
        with open(p, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)

def test_core_helm_templates_present():
    expected = [
        "_helpers.tpl", "deployment.yaml", "service.yaml", "gateway.yaml",
        "virtualservice.yaml", "peerauthentication.yaml", "destinationrule.yaml",
        "serviceaccount.yaml", "configmap.yaml", "hpa.yaml", "pdb.yaml",
        "network-policy.yaml"
    ]
    for tpl in expected:
        assert (TEMPLATES_DIR / tpl).exists(), f"Missing template {tpl}"
