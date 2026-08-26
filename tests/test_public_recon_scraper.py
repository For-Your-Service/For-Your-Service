#!/usr/bin/env python3
"""
Test Suite: Public Recon Scraper for Aerospace & Defense Talent
"""

import pytest
import os
import pandas as pd
from src.features.public_recon_scraper import PublicReconScraper, CURATED_PROFILES


def test_build_query_ge_aerospace():
    scraper = PublicReconScraper()
    query = scraper.build_query(
        company="GE Aerospace",
        role="Sr AI Data Engineer",
        location="Greenville, SC",
        branch="US Army"
    )
    
    assert "site:linkedin.com/in" in query
    assert "GE Aerospace" in query
    assert "Greenville" in query
    assert "US Army" in query or "Veteran" in query


def test_parse_linkedin_title_standard():
    scraper = PublicReconScraper()
    raw = "Christopher Ubillus - Plant Leader - GE Aerospace | LinkedIn"
    parsed = scraper.parse_linkedin_title(raw)
    
    assert parsed["name"] == "Christopher Ubillus"
    assert parsed["title"] == "Plant Leader"
    assert parsed["company"] == "GE Aerospace"


def test_detect_military_branch_and_clearance():
    scraper = PublicReconScraper()
    snippet_sf = "Retired Special Forces Green Beret with TS/SCI clearance and 20 years DoD experience."
    branch = scraper.detect_military_branch(snippet_sf)
    clearance = scraper.detect_clearance(snippet_sf)
    
    assert "Special Forces" in branch
    assert clearance == "TS/SCI"


def test_harvest_profiles_ge_aerospace():
    scraper = PublicReconScraper()
    profiles = scraper.harvest_profiles(
        company="GE Aerospace",
        role="Sr AI Data Engineer",
        location="Greenville, SC",
        max_results=5
    )
    
    assert len(profiles) >= 3
    assert any(p["name"] == "Christopher Ubillus" for p in profiles)
    assert any("GE Aerospace" in p["company"] for p in profiles)


def test_harvest_to_dataframe_and_csv(tmp_path):
    scraper = PublicReconScraper()
    csv_file = tmp_path / "test_contacts.csv"
    
    df = scraper.harvest_to_dataframe(
        company="GE Aerospace",
        role="Sr AI Data Engineer",
        location="Greenville, SC",
        output_csv_path=str(csv_file)
    )
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert os.path.exists(str(csv_file))
    
    # Reload and verify
    reloaded = pd.read_csv(str(csv_file))
    assert len(reloaded) == len(df)
    assert "name" in reloaded.columns
