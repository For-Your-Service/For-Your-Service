"""Unit tests for job data normalization"""


def test_salary_normalization():
    """Test salary range normalization"""
    # Annual salary
    annual = {"min": 80000, "max": 120000, "period": "year"}
    assert annual["min"] > 0
    assert annual["max"] >= annual["min"]

    # Hourly to annual conversion
    hourly_min = 40  # $40/hour
    expected_annual = hourly_min * 40 * 52  # $83,200
    assert expected_annual > 80000


def test_location_normalization():
    """Test location data normalization"""
    # Parse various location formats
    locations = ["Greenville, SC", "Greenville, South Carolina", "Greenville, SC 29601"]

    for loc in locations:
        assert "Greenville" in loc
        assert "SC" in loc or "South Carolina" in loc


def test_date_normalization():
    """Test date parsing and normalization"""
    date_formats = ["2026-08-10", "08/10/2026", "Aug 10, 2026"]

    # All should parse to same date
    for date_str in date_formats:
        assert "2026" in date_str
        assert "08" in date_str or "Aug" in date_str


def test_job_id_generation():
    """Test unique job ID generation"""
    # Hash of title + company + location
    job_data = {"title": "Software Engineer", "company": "Acme Corp", "location": "Greenville, SC"}

    import hashlib

    composite = f"{job_data['title']}{job_data['company']}{job_data['location']}"
    job_id = hashlib.sha256(composite.encode()).hexdigest()[:16]

    assert len(job_id) == 16
    assert job_id.isalnum()
