"""
Unit tests for the Universal Veteran Intake & Job Matching App
Tests branch-specific rank selection, MOS crosswalk lookup for all branches,
resume skill parsing, and zero-cost local matching engine.
"""

import pytest
from app.mos_data import lookup_mos, get_mos_choices_by_branch, MOS_DATABASE, BRANCH_RANKS
from app.sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILES, load_cached_scraped_jobs
from app.app import parse_veteran_skills, calculate_veteran_match_score


def test_all_branches_have_ranks():
    branches = ["Army", "Navy", "Air Force", "Marine Corps", "Coast Guard", "Space Force"]
    for b in branches:
        assert b in BRANCH_RANKS
        assert len(BRANCH_RANKS[b]) >= 10
        # Check enlisted and officer presence
        assert any("E-1" in r for r in BRANCH_RANKS[b])
        assert any("O-1" in r or "O-7" in r or "General" in r or "Admiral" in r for r in BRANCH_RANKS[b])


def test_mos_lookup_across_branches():
    # Army Special Forces & Combat
    sf = lookup_mos("18F")
    assert sf is not None
    assert sf["branch"] == "Army"
    
    inf = lookup_mos("11B")
    assert inf is not None
    assert "Infantry" in inf["title"]
    
    # Army Logistics & Mechanics
    log = lookup_mos("88M")
    assert log is not None
    assert "Motor Transport" in log["title"]
    
    # Navy IT & Ratings
    navy_it = lookup_mos("IT")
    assert navy_it is not None
    assert navy_it["branch"] == "Navy"
    
    # Air Force Cyber
    af = lookup_mos("1D7X1")
    assert af is not None
    assert af["branch"] == "Air Force"
    
    # Marine Corps
    marine = lookup_mos("0311")
    assert marine is not None
    assert marine["branch"] == "Marine Corps"


def test_mos_choices_filtering():
    army_choices = get_mos_choices_by_branch("Army")
    assert len(army_choices) >= 10
    assert all("(Army)" in c for c in army_choices)
    
    navy_choices = get_mos_choices_by_branch("Navy")
    assert len(navy_choices) >= 5
    assert all("(Navy)" in c for c in navy_choices)


def test_parse_veteran_skills_diverse():
    # Test Combat / Operations resume
    inf_text = """
    Infantry Squad Leader with 8 years active duty. Commanded 9-person tactical squad.
    Maintained 100% accountability for $1.5M in equipment. Expert in risk management and SOP compliance.
    """
    extracted_inf = parse_veteran_skills(inf_text, "11B")
    assert "risk management" in extracted_inf["leadership_skills"]
    assert "team leadership" in extracted_inf["mos_skills"]
    
    # Test Logistics / CDL resume
    log_text = """
    Motor Transport Operator with 6 years experience. Logged 80,000 incident-free miles on heavy tractor-trailers.
    Class A CDL equivalent, hazmat transport, preventive maintenance, and fleet dispatching.
    """
    extracted_log = parse_veteran_skills(log_text, "88M")
    assert "heavy vehicle operations" in extracted_log["mos_skills"]
    assert "cdl" in extracted_log["technical_skills"] or "dot compliance" in extracted_log["technical_skills"]


def test_calculate_veteran_match_score_all_profiles():
    for mos_key, profile in DEMO_VETERAN_PROFILES.items():
        extracted = parse_veteran_skills(profile["resume_text"], profile["mos"])
        sample_job = SAMPLE_JOBS[0]
        score, reasons = calculate_veteran_match_score(sample_job, profile, extracted)
        assert 30.0 <= score <= 100.0
        assert len(reasons) > 0


def test_load_cached_jobs_diversity():
    jobs = load_cached_scraped_jobs()
    assert len(jobs) >= len(SAMPLE_JOBS)
    
    categories = set(j.get("category", "") for j in jobs)
    assert len(categories) >= 3  # Multiple diverse job sectors
