"""
Pytest configuration and fixtures
"""

import pytest
from src.api.config import Config as APIConfig


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
    John Veteran
    john@example.com | (555) 123-4567 | Greenville, SC
    
    EXPERIENCE
    DevOps Engineer | Tech Company | 2020-Present
    - Deploy applications using Kubernetes and Docker
    - Manage AWS infrastructure with Terraform
    - Build CI/CD pipelines with Jenkins
    
    MILITARY SERVICE
    U.S. Army, Network Administrator (MOS 25B) | 2015-2020
    - Active TS/SCI clearance
    - Managed Cisco network infrastructure
    
    SKILLS
    Python, Bash, Docker, Kubernetes, AWS, Terraform
    """


@pytest.fixture
def mock_usajobs_response():
    """Mock USAJobs API response"""
    return {
        "SearchResult": {
            "SearchResultItems": [
                {
                    "MatchedObjectDescriptor": {
                        "PositionTitle": "Cybersecurity Specialist",
                        "OrganizationName": "Department of Defense",
                        "PositionLocationDisplay": "San Diego, CA",
                    }
                }
            ]
        }
    }


@pytest.fixture
def sample_job_description():
    """Sample job posting for testing."""
    return """
    Senior DevOps Engineer
    
    Requirements:
    - 5+ years experience with Kubernetes and Docker
    - Strong Terraform and AWS expertise
    - Python and Bash scripting
    - Security clearance preferred
    - Experience with Prometheus and Grafana
    """

