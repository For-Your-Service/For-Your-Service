#!/usr/bin/env python3
"""
Test Suite: LinkedIn Veteran Finder for Aerospace & Defense Engineering
"""

import pytest
from src.features.linkedin_veteran_finder import (
    LinkedInVeteranFinder,
    get_curated_ge_aerospace_targets,
    DEFAULT_COMPANIES,
    DEFAULT_ROLES,
    DEFAULT_LOCATIONS
)


def test_boolean_query_generation_ge_aerospace():
    finder = LinkedInVeteranFinder(
        company="GE Aerospace",
        role="Sr AI Data Engineer",
        location="Greenville, SC"
    )
    query = finder.generate_boolean_query()
    
    assert "site:linkedin.com/in" in query
    assert "GE Aerospace" in query
    assert "Greenville" in query
    assert "Veteran" in query or "Army" in query
    assert "Data Engineer" in query or "Sr AI Data Engineer" in query


def test_dynamic_arbitrary_inputs_boolean_query():
    # Test arbitrary user inputs
    finder = LinkedInVeteranFinder(
        company="Lockheed Martin, Boeing",
        role="DevSecOps Architect, Kubernetes Lead",
        location="Huntsville, AL, Dallas, TX",
        branch_filter="US Air Force"
    )
    query = finder.generate_boolean_query()
    
    assert "site:linkedin.com/in" in query
    assert "Lockheed Martin" in query
    assert "Boeing" in query
    assert "DevSecOps Architect" in query
    assert "Huntsville, AL" in query
    assert "US Air Force" in query


def test_search_urls_generation():
    finder = LinkedInVeteranFinder(
        company="GE Aerospace",
        role="Sr AI Data Engineer",
        location="Greenville, SC"
    )
    google_url = finder.generate_google_search_url()
    ddg_url = finder.generate_duckduckgo_url()
    li_url = finder.generate_direct_linkedin_search_url()
    
    assert google_url.startswith("https://www.google.com/search?q=")
    assert ddg_url.startswith("https://duckduckgo.com/?q=")
    assert li_url.startswith("https://www.linkedin.com/search/results/people/?keywords=")
    assert "GE+Aerospace" in google_url or "GE%20Aerospace" in google_url or "GE" in google_url


def test_search_talent_ledger_filtering():
    # Search for GE Aerospace veterans
    finder_ge = LinkedInVeteranFinder(company="GE Aerospace", role="Data Engineer", location="Greenville, SC")
    results_ge = finder_ge.search_talent_ledger(veteran_only=True)
    assert not results_ge.empty
    assert any("William Free Hall" in name for name in results_ge['name'])
    assert all(results_ge['is_veteran'] == True)
    
    # Search for Lockheed Martin veterans
    finder_lm = LinkedInVeteranFinder(company="Lockheed Martin", role="", location="")
    results_lm = finder_lm.search_talent_ledger(veteran_only=True)
    assert not results_lm.empty
    assert any("Lockheed Martin" in c for c in results_lm['company'])


def test_peer_outreach_message():
    finder = LinkedInVeteranFinder(company="GE Aerospace", role="Sr AI Data Engineer", location="Greenville, SC")
    msg = finder.generate_peer_outreach_message(
        peer_name="Alex",
        sender_name="Free Hall",
        sender_branch="US Army Special Forces (18F / 18Z, Ret.)",
        target_role="Sr AI Data Engineer"
    )
    
    assert "Hi Alex," in msg
    assert "GE Aerospace" in msg
    assert "18F / 18Z" in msg
    assert "Databricks/PySpark" in msg
    assert "Greenville, SC" in msg


def test_hiring_manager_outreach_message():
    finder = LinkedInVeteranFinder(company="GE Aerospace", role="Sr AI Data Engineer", location="Greenville, SC")
    msg = finder.generate_hiring_manager_outreach_message(
        manager_name="Sarah",
        sender_name="Free Hall",
        sender_title="Senior AI Data Engineer & Lakehouse Architect",
        target_role="Sr AI Data Engineer"
    )
    
    assert "Hi Sarah," in msg
    assert "GE Aerospace" in msg
    assert "Sr AI Data Engineer" in msg
    assert "Databricks Unity Catalog" in msg
    assert "https://fys-matching-app-7474643734871839.aws.databricksapps.com/" in msg


def test_curated_ge_aerospace_targets():
    targets = get_curated_ge_aerospace_targets()
    assert len(targets) >= 4
    for t in targets:
        assert "role" in t
        assert "company" in t
        assert t["company"] == "GE Aerospace"
        assert "location" in t
        assert "focus_areas" in t
        assert "boolean_sample" in t


def test_defaults_configuration():
    assert "GE Aerospace" in DEFAULT_COMPANIES
    assert "Sr AI Data Engineer" in DEFAULT_ROLES
    assert "Greenville, SC" in DEFAULT_LOCATIONS
