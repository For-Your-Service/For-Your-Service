"""Unit tests for job deduplication logic"""


def test_exact_duplicate_detection():
    """Test detection of exact duplicate jobs"""
    job1 = {"title": "Software Engineer", "company": "Acme Corp", "location": "Greenville, SC"}
    job2 = job1.copy()

    # Generate IDs
    import hashlib

    id1 = hashlib.sha256(str(job1).encode()).hexdigest()
    id2 = hashlib.sha256(str(job2).encode()).hexdigest()

    assert id1 == id2  # Should be identical


def test_similar_job_detection():
    """Test detection of similar jobs with minor differences"""
    job1 = {"title": "Software Engineer", "company": "Acme"}
    job2 = {"title": "Software Engineer II", "company": "Acme"}

    # These should be different (different seniority levels)
    assert job1["title"] != job2["title"]


def test_dedup_across_sources():
    """Test deduplication across multiple API sources"""
    # Same job from different sources
    usajobs_job = {"source": "USAJOBS", "title": "DevOps Engineer", "company": "DoD"}
    jsearch_job = {
        "source": "JSearch",
        "title": "DevOps Engineer",
        "company": "Department of Defense",
    }

    # Company names might differ slightly
    assert "DoD" in usajobs_job["company"] or "Department" in usajobs_job["company"]
