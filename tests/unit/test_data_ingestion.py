"""Unit tests for API data ingestion"""
import pytest
from unittest.mock import Mock, patch
from src.ingestion import fetch_indeed_jobs, parse_job_response, normalize_location


def test_parse_job_response():
    """Test parsing of Indeed API response"""
    api_response = {
        'results': [{
            'jobkey': 'abc123',
            'jobtitle': 'DevOps Engineer',
            'company': 'TechCorp',
            'formattedLocation': 'Greenville, SC',
            'snippet': 'Looking for experienced DevOps...',
            'date': '2026-08-05'
        }]
    }
    
    jobs = parse_job_response(api_response, source='indeed')
    
    assert len(jobs) == 1
    assert jobs[0]['job_id'] == 'indeed_abc123'
    assert jobs[0]['title'] == 'DevOps Engineer'
    assert jobs[0]['data_source'] == 'indeed'


def test_normalize_location():
    """Test location string normalization"""
    assert normalize_location('greenville, sc') == 'Greenville, SC'
    assert normalize_location('NEW YORK, NY') == 'New York, NY'
    assert normalize_location('San Francisco, CA') == 'San Francisco, CA'


@patch('requests.get')
def test_fetch_indeed_jobs_success(mock_get):
    """Test successful Indeed API call"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'results': []}
    mock_get.return_value = mock_response
    
    jobs = fetch_indeed_jobs(query='DevOps', location='Greenville, SC')
    
    assert isinstance(jobs, list)
    mock_get.assert_called_once()


@patch('requests.get')
def test_fetch_indeed_jobs_rate_limit(mock_get):
    """Test handling of rate limit response"""
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {'Retry-After': '60'}
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception, match="Rate limited"):
        fetch_indeed_jobs(query='DevOps', location='Greenville, SC')
