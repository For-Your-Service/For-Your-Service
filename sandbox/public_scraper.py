#!/usr/bin/env python3
"""
File: sandbox/public_scraper.py
Description: CLI Tool to Harvest Live LinkedIn Veteran Contacts for GE Aerospace Greenville
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Sandbox Isolation Protocol
"""

import sys
import os
import argparse
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add project root and sandbox to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.features.public_recon_scraper import PublicReconScraper

def main():
    parser = argparse.ArgumentParser(description="Harvest public LinkedIn veteran contacts for aerospace engineering.")
    parser.add_argument("--company", default="GE Aerospace", help="Target company name (default: GE Aerospace)")
    parser.add_argument("--role", default="Sr AI Data Engineer", help="Target role (default: Sr AI Data Engineer)")
    parser.add_argument("--location", default="Greenville, SC", help="Target location (default: Greenville, SC)")
    parser.add_argument("--branch", default="All Veterans", help="Military branch filter")
    parser.add_argument("--export", default="sandbox/mock_data.csv", help="Output CSV path")
    args = parser.parse_args()

    print("=" * 80)
    print(" 🎯 PUBLIC VETERAN RECONNAISSANCE SCRAPER")
    print(f" Target: {args.company} | Location: {args.location} | Role: {args.role}")
    print("=" * 80)

    scraper = PublicReconScraper()
    df = scraper.harvest_to_dataframe(
        company=args.company,
        role=args.role,
        location=args.location,
        branch=args.branch,
        output_csv_path=args.export
    )

    print(f"\n[+] Successfully harvested {len(df)} contacts matching criteria!")
    print("-" * 80)
    
    for idx, row in df.iterrows():
        print(f" [{idx + 1}] NAME: {row['name']}")
        print(f"     ROLE:     {row['title']} @ {row['company']}")
        print(f"     LOCATION: {row['location']}")
        print(f"     BRANCH:   {row['branch']} | CLEARANCE: {row['clearance']}")
        print(f"     LINK:     {row['profile_url']}")
        print(f"     NOTE (<300 char): Hi {row['name'].split()[0]}, saw you're making waves at {row['company']} in Greenville. As a retired Special Forces Green Beret / Tech Lead transitioning into senior data engineering, I'd love to swap notes for 10 minutes.")
        print("-" * 80)

    print(f"\n[OK] Contacts saved to '{args.export}'")

if __name__ == "__main__":
    main()
