#!/usr/bin/env python3
"""API Rate Limit Checker for For Your Service"""
import requests
import os
from datetime import datetime

def check_usajobs_quota():
    print("📊 USAJOBS API")
    print("   Limit: 1000 requests/day")
    print("   Status: ✅ Track via logs")
    
def check_jsearch_quota(api_key):
    print("\n📊 JSearch API")
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    try:
        response = requests.get(
            "https://jsearch.p.rapidapi.com/search",
            headers=headers,
            params={"query": "test", "num_pages": "1"},
            timeout=10
        )
        remaining = response.headers.get('X-RateLimit-Remaining', 'Unknown')
        print(f"   Remaining: {remaining}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    print("🔍 API Rate Limit Check")
    print(f"Date: {datetime.now()}")
    check_usajobs_quota()
