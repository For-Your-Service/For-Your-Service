"""
Test suite for verifying Helm chart structure, YAML integrity, and Istio Service Mesh configurations.
"""

from pathlib import Path
import yaml
import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
CHARTS_DIR = REPO_ROOT / "charts" / "for-your-service"
TEMPLATES_DIR = CHARTS_DIR / "templates"
DEPLOYMENT_ISTIO_DIR = REPO_ROOT / "deployment" / "kubernetes" / "istio"


def test_chart_yaml_exists_and_valid():
    chart_file = CHARTS_DIR / "Chart.yaml"
    assert chart_file.exists(), "Chart.yaml does not exist in charts/for-your-service"

    with open(chart_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("apiVersion") == "v2"
    assert data.get("name") == "for-your-service"
    assert "version" in data
    assert "appVersion" in data
    assert "description" in data


def test_values_yaml_exists_and_valid():
    values_file = CHARTS_DIR / "values.yaml"
    assert values_file.exists(), "values.yaml does not exist in charts/for-your-service"

    with open(values_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert "replicaCount" in data
    assert data["replicaCount"] >= 1
    assert "image" in data
    assert "repository" in data["image"]
    assert "istio" in data
    assert data["istio"].get("enabled") is True
    assert data["istio"]["mtls"].get("mode") == "STRICT"
    assert "gateway" in data["istio"]
    assert "virtualService" in data["istio"]


def test_helm_templates_exist():
    expected_templates = [
        "_helpers.tpl",
        "deployment.yaml",
        "service.yaml",
        "gateway.yaml",
        "virtualservice.yaml",
        "peerauthentication.yaml",
        "destinationrule.yaml",
        "serviceaccount.yaml",
        "configmap.yaml",
        "hpa.yaml",
    ]

    for template_name in expected_templates:
        tpl_path = TEMPLATES_DIR / template_name
        assert tpl_path.exists(), f"Helm template {template_name} is missing in {TEMPLATES_DIR}"


def test_standalone_istio_manifests_valid():
    expected_manifests = [
        ("gateway.yaml", "Gateway", "networking.istio.io/v1beta1"),
        ("virtualservice.yaml", "VirtualService", "networking.istio.io/v1beta1"),
        ("peer-authentication.yaml", "PeerAuthentication", "security.istio.io/v1beta1"),
        ("destination-rule.yaml", "DestinationRule", "networking.istio.io/v1beta1"),
        ("canary-virtualservice.yaml", "VirtualService", "networking.istio.io/v1beta1"),
    ]

    for filename, expected_kind, expected_api_version in expected_manifests:
        file_path = DEPLOYMENT_ISTIO_DIR / filename
        assert file_path.exists(), f"Standalone Istio manifest {filename} missing"

        with open(file_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)

        assert manifest.get("kind") == expected_kind, f"{filename} kind mismatch"
        assert manifest.get("apiVersion") == expected_api_version, f"{filename} apiVersion mismatch"


def test_peer_authentication_strict_mode():
    pa_file = DEPLOYMENT_ISTIO_DIR / "peer-authentication.yaml"
    with open(pa_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["spec"]["mtls"]["mode"] == "STRICT", "Zero-Trust mTLS mode must be STRICT"


def test_virtual_service_routing_configuration():
    vs_file = DEPLOYMENT_ISTIO_DIR / "virtualservice.yaml"
    with open(vs_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert "spec" in data
    assert "hosts" in data["spec"]
    assert "gateways" in data["spec"]
    assert "http" in data["spec"]
    routes = data["spec"]["http"][0]["route"]
    assert any("streamlit-frontend" in r["destination"]["host"] for r in routes)


def test_canary_virtual_service_traffic_splitting():
    canary_file = DEPLOYMENT_ISTIO_DIR / "canary-virtualservice.yaml"
    with open(canary_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    routes = data["spec"]["http"][0]["route"]
    assert len(routes) == 2, "Canary VirtualService should define two route destinations"
    weights = [r.get("weight") for r in routes]
    assert 90 in weights
    assert 10 in weights
    assert sum(weights) == 100


def test_implementation_checklist_doc_exists():
    checklist_file = REPO_ROOT / "helm_istio_implementation.md"
    assert checklist_file.exists(), "helm_istio_implementation.md does not exist"

    content = checklist_file.read_text(encoding="utf-8")
    assert "Step 1: Helm Migration" in content
    assert "Step 2: Pipeline Update" in content
    assert "Step 3: Istio Mesh Injection" in content
    assert "Step 4: Zero-Trust Policy" in content
    assert "Step 5: Routing Rules" in content
