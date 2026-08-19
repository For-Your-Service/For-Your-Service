"""
Unit tests for the Veteran Intake & Job Matching App
Tests MOS crosswalk lookup, skill parsing, and zero-cost local matching engine.
"""

import pytest
from app.mos_data import lookup_mos, get_all_mos_choices, MOS_DATABASE
from app.sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILE, load_cached_scraped_jobs
from app.app import parse_veteran_skills, calculate_veteran_match_score


def test_mos_lookup_exact():
    res = lookup_mos("18F")
    assert res is not None
    assert res["code"] == "18F"
    assert "Intelligence" in res["title"]
    assert res["branch"] == "Army"
    assert "intelligence analysis" in res["transferable_skills"]


def test_mos_lookup_case_insensitive_and_prefix():
    res = lookup_mos("mos 25b")
    assert res is not None
    assert res["code"] == "25B"
    assert "Information Technology" in res["title"]


def test_mos_choices():
    choices = get_all_mos_choices()
    assert len(choices) >= 15
    assert any("18Z" in c for c in choices)
    assert any("IT" in c for c in choices)
    assert any("1D7X1" in c for c in choices)


def test_parse_veteran_skills():
    sample_text = """
    William Free Hall
    DevOps Engineer with 10+ years experience in AWS, Kubernetes, Terraform, Docker, Python, and Databricks.
    Led cross-functional teams in mission planning and executive briefings.
    """
    extracted = parse_veteran_skills(sample_text, "18F")
    assert "aws" in extracted["technical_skills"]
    assert "kubernetes" in extracted["technical_skills"]
    assert "python" in extracted["technical_skills"]
    assert "executive briefings" in extracted["leadership_skills"]
    assert extracted["total_years"] >= 10
    assert "Senior" in extracted["seniority"]


def test_calculate_veteran_match_score():
    sample_job = SAMPLE_JOBS[0]  # Lead Cloud Solutions Architect
    extracted = parse_veteran_skills(DEMO_VETERAN_PROFILE["resume_text"], DEMO_VETERAN_PROFILE["mos"])
    score, reasons = calculate_veteran_match_score(sample_job, DEMO_VETERAN_PROFILE, extracted)
    
    assert 50.0 <= score <= 100.0
    assert len(reasons) > 0
    assert any("Technical Match" in r or "Direct MOS Crosswalk" in r or "Skills" in r for r in reasons)


def test_load_cached_jobs():
    jobs = load_cached_scraped_jobs()
    assert len(jobs) >= len(SAMPLE_JOBS)
    for j in jobs:
        assert "title" in j
        assert "company" in j
        assert "salary_min" in j
        assert "salary_max" in j
