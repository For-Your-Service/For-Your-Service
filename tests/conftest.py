"""
Pytest configuration and fixtures
"""

import pytest
from src.api.config import Config as APIConfig


@pytest.fixture
def api_config():
    """Mock API configuration for testing"""
    return APIConfig()


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
