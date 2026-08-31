"""Unit tests for For-Your-Service Autonomous Build Flywheel."""

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_flywheel_directories_exist():
    """Verify all 8 core flywheel directories exist."""
    required_dirs = [
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "engine",
        PROJECT_ROOT / "ingestors",
        PROJECT_ROOT / "ui",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "data/raw",
        PROJECT_ROOT / "data/processed",
        PROJECT_ROOT / ".github/workflows",
    ]
    for d in required_dirs:
        assert d.exists(), f"Required flywheel directory missing: {d}"


def test_stage2_data_ingestion():
    """Test Stage 2 Live Real-World Data Ingestor."""
    ingestor_script = PROJECT_ROOT / "scripts/02_live_data_ingestor.py"
    assert ingestor_script.exists()

    res = subprocess.run([sys.executable, str(ingestor_script)], capture_output=True, text=True)
    assert res.returncode == 0, f"Ingestion failed: {res.stderr}"

    raw_file = PROJECT_ROOT / "data/raw/live_federal_jobs.json"
    assert raw_file.exists(), "live_federal_jobs.json was not created"

    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "SearchResult" in data
    items = data.get("SearchResult", {}).get("SearchResultItems", [])
    assert len(items) > 0, "No job items found in payload"


def test_stage4_docs_topology_sync():
    """Test Stage 4 Self-Updating Architecture Docs & Mermaid Generator."""
    sync_script = PROJECT_ROOT / "scripts/04_sync_docs.py"
    assert sync_script.exists()

    res = subprocess.run([sys.executable, str(sync_script)], capture_output=True, text=True)
    assert res.returncode == 0, f"Docs sync failed: {res.stderr}"

    topology_file = PROJECT_ROOT / "docs/SYSTEM_TOPOLOGY.md"
    assert topology_file.exists()

    content = topology_file.read_text(encoding="utf-8")
    assert "mermaid" in content
    assert "Live System Topology" in content
    assert "PySpark Vector Pipeline" in content
