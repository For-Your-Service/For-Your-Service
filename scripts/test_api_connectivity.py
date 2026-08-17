#!/usr/bin/env python3
"""Test API connectivity for all sources"""

import requests


def test_usajobs(api_key, user_agent):
    url = "https://data.usajobs.gov/api/search"
    headers = {"Host": "data.usajobs.gov", "User-Agent": user_agent, "Authorization-Key": api_key}
    try:
        response = requests.get(url, headers=headers, params={"Keyword": "test"}, timeout=10)
        return response.status_code == 200
    except:
        return False


def test_jsearch(api_key):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    try:
        response = requests.get(url, headers=headers, params={"query": "test"}, timeout=10)
        return response.status_code == 200
    except:
        return False


def test_adzuna(app_id, app_key):
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {"app_id": app_id, "app_key": app_key, "what": "test"}
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.status_code == 200
    except:
        return False


if __name__ == "__main__":
    print("🔌 Testing API Connectivity...")
    # Add your API keys here or load from environment
    print("✅ Test script ready")
