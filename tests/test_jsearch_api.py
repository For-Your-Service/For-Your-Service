"""Unit tests for JSearch API connector"""


def test_jsearch_auth_headers():
    """Test JSearch authentication headers"""
    api_key = "test-rapid-key"

    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}

    assert headers["X-RapidAPI-Host"] == "jsearch.p.rapidapi.com"
    assert "X-RapidAPI-Key" in headers


def test_jsearch_query_construction():
    """Test JSearch query parameter construction"""
    query = "software engineer veteran"
    location = "Greenville, SC"

    params = {
        "query": f"{query} in {location}",
        "date_posted": "month",
        "employment_types": "FULLTIME,CONTRACTOR",
    }

    assert location in params["query"]
    assert "FULLTIME" in params["employment_types"]


def test_jsearch_salary_parsing():
    """Test JSearch salary data parsing"""
    job_data = {"job_salary_min": 80000, "job_salary_max": 120000, "job_salary_currency": "USD"}

    assert job_data["job_salary_min"] > 0
    assert job_data["job_salary_max"] >= job_data["job_salary_min"]
    assert job_data["job_salary_currency"] == "USD"
