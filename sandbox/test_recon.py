#!/usr/bin/env python3
"""
Test Suite: Sandbox Reconnaissance Engine & Dynamic Filtering
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Sandbox Isolation Protocol
"""

import pytest
import pandas as pd
import os
import sys

# Ensure sandbox directory is testable independently
SANDBOX_DIR = os.path.dirname(__file__)
if SANDBOX_DIR not in sys.path:
    sys.path.insert(0, SANDBOX_DIR)

from recon_app import load_sandbox_ledger, generate_sandbox_boolean_query


def test_load_sandbox_ledger_exists_and_populated():
    df = load_sandbox_ledger()
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 3
    expected_cols = ["name", "company", "title", "location", "branch", "clearance", "is_veteran"]
    for col in expected_cols:
        assert col in df.columns


def test_dynamic_filtering_ge_aerospace_greenville():
    df = load_sandbox_ledger()
    
    # Filter for GE Aerospace in Greenville, SC
    mask = (
        df['company'].str.contains("GE", case=False, na=False) &
        df['title'].str.contains("AI|Data", case=False, na=False) &
        df['location'].str.contains("Greenville", case=False, na=False) &
        (df['is_veteran'] == True)
    )
    results = df[mask]
    
    assert not results.empty
    assert any("William Free Hall" in name for name in results['name'])
    assert all(results['company'] == "GE Aerospace")


def test_dynamic_filtering_lockheed_martin():
    df = load_sandbox_ledger()
    
    mask = (
        df['company'].str.contains("Lockheed", case=False, na=False) &
        (df['is_veteran'] == True)
    )
    results = df[mask]
    
    assert not results.empty
    assert any("Elena Rostova" in name for name in results['name'])


def test_veteran_only_enforcement():
    df = load_sandbox_ledger()
    
    # Sarah Connor is marked as civilian (is_veteran == False)
    mask_all = df['name'].str.contains("Sarah Connor")
    assert any(df[mask_all]['is_veteran'] == False)
    
    # When filtering is_veteran == True, Sarah Connor must be excluded
    mask_vet = (df['is_veteran'] == True) & df['name'].str.contains("Sarah Connor")
    assert df[mask_vet].empty


def test_generate_sandbox_boolean_query():
    query = generate_sandbox_boolean_query(
        company="GE Aerospace",
        role="Sr AI Data Engineer",
        location="Greenville, SC",
        branch="US Army"
    )
    
    assert "site:linkedin.com/in" in query
    assert "GE Aerospace" in query
    assert "Greenville" in query
    assert "US Army" in query or "Veteran" in query
