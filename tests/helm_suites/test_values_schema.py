"""
Test suite verifying Helm values.schema.json conformance.
"""
from pathlib import Path
import json
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CHART_DIR = REPO_ROOT / "charts" / "for-your-service"

def test_schema_json_valid():
    schema_file = CHART_DIR / "values.schema.json"
    assert schema_file.exists()
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema.get("type") == "object"
    assert "replicaCount" in schema.get("properties", {})
