#!/usr/bin/env python3
"""
For Your Service - API Testing Script
Tests the Hugging Face Spaces API backend

Developer: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
Date: 2026-08-09
"""

import requests
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "https://YOUR_USERNAME-for-your-service-api.hf.space"
# Update with your actual Hugging Face Space URL after deployment


def test_health_check():
    """Test health check endpoint"""
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)

    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✅ PASS: Health check successful")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_root_endpoint():
    """Test root endpoint"""
    print("\n" + "=" * 60)
    print("TEST 2: Root Endpoint Info")
    print("=" * 60)

    try:
        response = requests.get(API_BASE_URL)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✅ PASS: Root endpoint successful")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_register_veteran():
    """Test veteran registration"""
    print("\n" + "=" * 60)
    print("TEST 3: Register Veteran")
    print("=" * 60)

    veteran_data = {
        "name": "John Veteran",
        "email": "john.veteran@example.com",
        "location": {"target_city": "Houston", "target_state": "TX"},
        "experience_summary": {"total_years": 10, "seniority_level": "Mid"},
        "technical_skills": {
            "expert": ["AWS", "Docker"],
            "proficient": ["Python", "Jenkins"],
            "familiar": ["Kubernetes"],
        },
        "target_roles": ["DevOps Engineer", "Cloud Engineer"],
        "salary_requirements": {"min": 100000, "target": 130000, "max": 160000},
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/veteran/register",
            json=veteran_data,
            headers={"Content-Type": "application/json"},
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            veteran_id = response.json().get("veteran_id")
            print(f"✅ PASS: Veteran registered with ID: {veteran_id}")
            return veteran_id
        else:
            print(f"❌ FAIL: Registration failed")
            return None
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return None


def test_get_veteran(veteran_id):
    """Test get veteran profile"""
    print("\n" + "=" * 60)
    print("TEST 4: Get Veteran Profile")
    print("=" * 60)

    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/veteran/{veteran_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✅ PASS: Veteran profile retrieved")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_job_matching(veteran_id):
    """Test job matching endpoint"""
    print("\n" + "=" * 60)
    print("TEST 5: Job Matching")
    print("=" * 60)

    match_request = {
        "veteran_id": veteran_id,
        "top_n": 10,
        "location_filter": "Houston",
        "min_score": 0.5,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/match",
            json=match_request,
            headers={"Content-Type": "application/json"},
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Total Matches: {result.get('total_matches', 0)}")

        if result.get("matches"):
            print(f"\nTop 3 Matches:")
            for i, match in enumerate(result["matches"][:3], 1):
                print(f"{i}. {match['title']} at {match['company']}")
                print(f"   Match Score: {match['match_score']:.2f}")
                print(f"   Location: {match['location']}")

        print("✅ PASS: Job matching successful")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def test_search_jobs():
    """Test job search endpoint"""
    print("\n" + "=" * 60)
    print("TEST 6: Search Jobs")
    print("=" * 60)

    try:
        response = requests.get(
            f"{API_BASE_URL}/api/v1/jobs", params={"location": "Houston", "limit": 5}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Total Jobs: {result.get('total', 0)}")

        if result.get("jobs"):
            print(f"\nSample Jobs:")
            for i, job in enumerate(result["jobs"][:3], 1):
                print(f"{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")

        print("✅ PASS: Job search successful")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False


def run_all_tests():
    """Run all API tests"""
    print("\n" + "=" * 70)
    print("🧪 FOR YOUR SERVICE - API TESTING SUITE")
    print("=" * 70)
    print(f"API URL: {API_BASE_URL}")
    print(f"Test Run: {datetime.now().isoformat()}")
    print("=" * 70)

    results = {
        "health_check": test_health_check(),
        "root_endpoint": test_root_endpoint(),
    }

    # Register veteran and get ID for subsequent tests
    veteran_id = test_register_veteran()
    if veteran_id:
        results["register_veteran"] = True
        results["get_veteran"] = test_get_veteran(veteran_id)
        results["job_matching"] = test_job_matching(veteran_id)
    else:
        results["register_veteran"] = False
        results["get_veteran"] = False
        results["job_matching"] = False

    results["search_jobs"] = test_search_jobs()

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status}: {test_name}")

    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ SOME TESTS FAILED - Review output above")


if __name__ == "__main__":
    # Update API_BASE_URL before running!
    if "YOUR_USERNAME" in API_BASE_URL:
        print("❌ ERROR: Update API_BASE_URL with your Hugging Face Space URL!")
        print("Example: https://freehall-for-your-service-api.hf.space")
    else:
        run_all_tests()
