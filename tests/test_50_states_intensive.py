"""
Intensive 50-State Comprehensive Location & Distance Validation Test Suite
For Your Service - 7 Eagle Group
Validates that every state, major metropolitan area, and commute radius (up to 200 miles)
strictly targets the user-supplied location and prevents any static/hardcoded data contamination.
"""

import pytest
from app.geo_database import CITY_COORDINATES, lookup_city_coordinates
from app.app import estimate_job_distance, calculate_veteran_match_score, parse_veteran_skills
from app.sample_data import load_cached_scraped_jobs, generate_localized_partner_jobs

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
    3. Verifies that generated local jobs strictly match the candidate's target city/state at 0 miles.
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

        # Load jobs dynamically driven by candidate's location input
        jobs = load_cached_scraped_jobs(target_city=city, target_state=state, target_track=profile["target_track"])

        # Find the localized job generated for this city
        local_jobs = [j for j in jobs if j.get("city", "").lower() == city.lower() and j.get("state", "").upper() == state.upper()]
        assert len(local_jobs) > 0, f"No localized jobs generated for target input: {city}, {state}"

        # Evaluate the localized job
        local_job = local_jobs[0]
        score, reasons, factors = calculate_veteran_match_score(local_job, profile, extracted)

        # Assert local job gets a top score and distance is 0.0 or <= radius
        dist = factors["location"]["distance_miles"]
        assert dist is not None and dist <= float(radius), f"Local job for {city}, {state} calculated distance {dist} > {radius}"
        assert factors["location"]["status"] == "pass", f"Local job for {city}, {state} failed location check: {factors['location']}"
        assert score >= 75.0, f"Local job match score too low ({score}) for {city}, {state}"

        # Evaluate an out-of-region non-remote job (e.g. if candidate is NOT in Miami FL, test Miami FL job as out-of-region)
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
            # If distance is > radius, verify the location status is flagged as warn / out-of-region
            if d_dist > float(radius):
                _, _, d_factors = calculate_veteran_match_score(distant_job, profile, extracted)
                assert d_factors["location"]["status"] in ("fail", "warn"), f"Distant job in Tampa FL was not flagged out-of-region for candidate in {city}, {state} (dist={d_dist}, radius={radius})"
                assert "Outside" in d_factors["location"]["detail"], f"Expected 'Outside' in detail for {city}, {state}, got: {d_factors['location']['detail']}"
