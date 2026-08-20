#!/usr/bin/env python3
"""
File: scripts/test_usajobs_search.py
Description: CLI Tool to test live USAJOBS Search Ingestion for Bronze Layer
Lead Architect: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingestion.usajobs_ingestor import USAJobsIngestor

def main():
    print("=================================================================")
    print(" USAJOBS Live Search Ingestion Test - Bronze Layer")
    print("=================================================================")
    
    api_key = os.getenv("USAJOBS_API_KEY")
    email = os.getenv("USAJOBS_EMAIL", "whall4.wh@gmail.com")
    
    if not api_key:
        print("[!] Note: USAJOBS_API_KEY is not set.")
        print("    To run with your developer key:")
        print("      $env:USAJOBS_API_KEY=\"your_key_here\"")
        print("      $env:USAJOBS_EMAIL=\"whall4.wh@gmail.com\"")
        print("      python scripts/test_usajobs_search.py\n")
        return
        
    ingestor = USAJobsIngestor(api_key=api_key, email=email)
    
    # 1. Fetch live listings
    raw_data = ingestor.fetch_jobs(keyword="Information Technology", location="Greenville, SC", results_per_page=10)
    
    if not raw_data:
        print("[!] No data returned or request failed.")
        return
        
    items = raw_data.get("SearchResult", {}).get("SearchResultItems", [])
    print(f"\n[✓] Received {len(items)} raw listings.")
    
    # 2. Transform to Bronze Layer Schema
    bronze_records = ingestor.transform_to_bronze(items)
    print(f"[✓] Transformed {len(bronze_records)} records to workspace.fys_bronze.job_postings format.\n")
    
    for idx, job in enumerate(bronze_records[:3], 1):
        print(f"--- [Job #{idx}] ---")
        print(f" Title:       {job['title']}")
        print(f" Agency:      {job['company']}")
        print(f" Location:    {job['location']}")
        print(f" Salary:      ${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}")
        print(f" Clearance:   {job['clearance_required']}")
        print(f" Apply URL:   {job['application_url']}\n")

if __name__ == "__main__":
    main()
