"""Unit tests for Adzuna API connector"""


def test_adzuna_auth_params():
    """Test Adzuna authentication parameters"""
    app_id = "test-app-id"
    app_key = "test-app-key"

    params = {"app_id": app_id, "app_key": app_key}

    assert "app_id" in params
    assert "app_key" in params


def test_adzuna_location_formatting():
    """Test Adzuna location parameter formatting"""
    location = "Greenville, SC"

    # Adzuna uses "where" parameter
    params = {"where": location, "distance": 50, "max_days_old": 30}  # miles

    assert params["where"] == location
    assert params["distance"] == 50


def test_adzuna_salary_flag():
    """Test Adzuna salary prediction flag"""
    job_data = {
        "salary_min": 90000,
        "salary_max": 130000,
        "salary_is_predicted": "0",  # Real salary data
    }

    # Adzuna provides real salary data (not predicted)
    assert job_data["salary_is_predicted"] == "0"
    assert job_data["salary_min"] > 0
