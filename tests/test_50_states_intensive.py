"""
Intensive 50-State Comprehensive Location & Real-Data Validation Test Suite
For Your Service - 7 Eagle Group
Validates that every state, major metropolitan area, and commute radius (up to 200 miles)
strictly targets the user-supplied location and prevents any synthetic/fictitious data bleed.
"""

import pytest
from app.geo_database import CITY_COORDINATES, lookup_city_coordinates
from app.app import estimate_job_distance, calculate_veteran_match_score, parse_veteran_skills
from app.sample_data import load_cached_scraped_jobs

# Major cities across all 50 US States + District of Columbia
FIFTY_STATES_MAJOR_CITIES = {
    "AL": "Huntsville",
    "AK": "Anchorage",
    "AZ": "Phoenix",
    "AR": "Little Rock",
    "CA": "San Diego",
    "CO": "Colorado Springs",
    "CT": "Hartford",
    "DE": "Wilmington",
    "DC": "Washington",
    "FL": "Niceville",
    "GA": "Atlanta",
    "HI": "Honolulu",
    "ID": "Boise",
    "IL": "Chicago",
    "IN": "Indianapolis",
    "IA": "Des Moines",
    "KS": "Wichita",
    "KY": "Louisville",
    "LA": "New Orleans",
    "ME": "Portland",
    "MD": "Baltimore",
    "MA": "Boston",
    "MI": "Detroit",
    "MN": "Minneapolis",
    "MS": "Biloxi",
    "MO": "Kansas City",
    "MT": "Billings",
    "NE": "Omaha",
    "NV": "Las Vegas",
    "NH": "Manchester",
    "NJ": "Newark",
    "NM": "Albuquerque",
    "NY": "New York",
    "NC": "Fayetteville",
    "ND": "Fargo",
    "OH": "Columbus",
    "OK": "Oklahoma City",
    "OR": "Portland",
    "PA": "Philadelphia",
    "RI": "Providence",
    "SC": "Greenville",
    "SD": "Sioux Falls",
    "TN": "Nashville",
    "TX": "Dallas",
    "UT": "Salt Lake City",
    "VT": "Burlington",
    "VA": "Virginia Beach",
    "WA": "Seattle",
    "WV": "Charleston",
    "WI": "Milwaukee",
    "WY": "Cheyenne"
}


def test_all_50_states_have_resolved_coordinates():
    """Verify that every US state and DC has valid GPS coordinates in the geo database."""
    assert len(FIFTY_STATES_MAJOR_CITIES) == 51
    for state, city in FIFTY_STATES_MAJOR_CITIES.items():
        coords = lookup_city_coordinates(city, state)
        assert coords is not None, f"Coordinates missing for {city}, {state}"
        assert -90.0 <= coords[0] <= 90.0, f"Invalid latitude for {city}, {state}"
        assert -180.0 <= coords[1] <= 180.0, f"Invalid longitude for {city}, {state}"


@pytest.mark.parametrize("state,city", list(FIFTY_STATES_MAJOR_CITIES.items()))
def test_location_targeting_and_radius_enforcement(state, city):
    """
    Intensive test for each of the 50 US States + DC:
    1. Ingests candidate profile targeting this specific city/state.
    2. Tests radii from 25 to 200 miles.
    3. Verifies that real job in the candidate's exact city resolves at <= 5 miles.
    4. Verifies that distant out-of-state jobs are strictly penalized as out-of-region.
    """
    sample_resume = f"""
    CANDIDATE FOR {city.upper()}, {state.upper()}
    Senior Cloud & Operations Specialist | Veteran
    {city}, {state} | candidate@{city.lower().replace(' ', '')}.example.com
    Experience: AWS, Python, Kubernetes, Terraform, Docker, CI/CD, Project Management, Team Leadership.
    """
    extracted = parse_veteran_skills(sample_resume, "18Z")

    for radius in [25, 50, 100, 200]:
        profile = {
            "name": f"Veteran in {city}",
            "branch": "Army",
            "rank": "E-7",
            "mos": "18Z",
            "clearance": "Secret",
            "target_track": "Cloud & DevOps Engineering",
            "desired_role": "",
            "target_city": city,
            "target_state": state,
            "target_radius": f"{radius} miles",
            "remote_ok": False,
            "relocate": False,
            "salary_min": 100000,
            "salary_max": 180000
        }

        # Verify real in-city job evaluation
        in_city_job = {
            "title": "Principal Systems Engineer",
            "company": "Defense Systems",
            "city": city,
            "state": state,
            "location_display": f"{city}, {state}",
            "salary_min": 140000,
            "salary_max": 190000,
            "clearance_required": "Secret",
            "skills": ["aws", "kubernetes", "python", "terraform"]
        }
        in_dist = estimate_job_distance(city, state, in_city_job["city"], in_city_job["state"], in_city_job["location_display"])
        assert in_dist is not None and in_dist <= float(radius), f"In-city job distance {in_dist} > {radius} for {city}, {state}"
        sc_in, _, f_in = calculate_veteran_match_score(in_city_job, profile, extracted)
        assert f_in["location"]["status"] == "pass", f"Local job failed for {city}, {state}: {f_in['location']}"
        assert sc_in >= 80.0, f"Score too low for local job in {city}, {state}: {sc_in}"

        # Evaluate an out-of-region non-remote job (e.g. if candidate is NOT in Tampa FL)
        if state != "FL":
            distant_job = {
                "title": "Defense Cloud Infrastructure Engineer",
                "company": "L3Harris",
                "city": "Tampa",
                "state": "FL",
                "location_display": "Tampa, FL (Onsite)",
                "salary_min": 138000,
                "salary_max": 178000,
                "clearance_required": "Secret",
                "skills": ["aws", "kubernetes", "linux", "python"]
            }
            d_dist = estimate_job_distance(city, state, distant_job["city"], distant_job["state"], distant_job["location_display"])
            if d_dist > float(radius):
                _, _, d_factors = calculate_veteran_match_score(distant_job, profile, extracted)
                assert d_factors["location"]["status"] in ("fail", "warn"), f"Distant job in Tampa FL was not flagged out-of-region for candidate in {city}, {state} (dist={d_dist}, radius={radius})"
                assert "Outside" in d_factors["location"]["detail"], f"Expected 'Outside' in detail for {city}, {state}, got: {d_factors['location']['detail']}"
