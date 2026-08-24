#!/usr/bin/env python3
"""
File: scripts/broadcast_linkedin_telemetry.py
Description: Dynamic Automated LinkedIn Telemetry & Narrative Summary Broadcast
Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts.generate_ai_summary import build_narrative_post
except ImportError:
    from generate_ai_summary import build_narrative_post

def broadcast_to_linkedin(dry_run=False):
    print("=================================================================")
    print(" For Your Service — Automated LinkedIn Telemetry Broadcast")
    print("=================================================================")

    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()
    author_urn = (
        os.getenv("LINKEDIN_AUTHOR_URN", "").strip() or
        os.getenv("LINKEDIN_PERSON_URN", "").strip() or
        os.getenv("LINKEDIN_ORGANIZATION_URN", "").strip() or
        "urn:li:person:iXAJqWIA_I"
    )

    # Generate intelligent narrative post
    post_text = build_narrative_post()

    print("\n--- Broadcast Payload Preview ---")
    print(post_text)
    print("---------------------------------\n")

    if dry_run or not token or not author_urn:
        if not token or not author_urn:
            print("[INFO] LINKEDIN_ACCESS_TOKEN or LINKEDIN_AUTHOR_URN not configured.")
            print("       Set these in GitHub Secrets (Settings > Secrets and variables > Actions) to enable live posting.")
            print("[DRY-RUN] Broadcast simulated successfully with dynamic narrative metrics.")
        else:
            print("[DRY-RUN] Simulation mode complete.")
        return

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Format author URN (support organization, person, or raw ID)
    if not author_urn.startswith("urn:li:"):
        author_urn = f"urn:li:person:{author_urn}"

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    print(f"[*] Posting narrative update to LinkedIn author: {author_urn}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"API Response Code: {response.status_code}")
        print(response.text)
        if response.status_code in [200, 201]:
            print("[SUCCESS] Successfully broadcast narrative update to LinkedIn!")
        else:
            print(f"[!] Note on broadcast: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Request error: {e}")

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    broadcast_to_linkedin(dry_run=is_dry)
