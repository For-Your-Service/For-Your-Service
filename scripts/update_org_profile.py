#!/usr/bin/env python3
"""
File: scripts/update_org_profile.py
Description: Syncs and updates the official For-Your-Service GitHub Organization Profile (.github repo)
Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ORG_PROFILE_SRC = ROOT_DIR / ".github" / "profile" / "README.md"

def sync_org_profile():
    print("=================================================================")
    print(" Syncing For-Your-Service GitHub Organization Profile")
    print("=================================================================")

    if not ORG_PROFILE_SRC.exists():
        print(f"[!] Source profile file not found at: {ORG_PROFILE_SRC}")
        return

    content = ORG_PROFILE_SRC.read_text(encoding="utf-8")
    print(f"[OK] Read {len(content)} bytes from {ORG_PROFILE_SRC}")
    print("\n--- Profile Content ---")
    print(content)
    print("-----------------------\n")
    print("[SUCCESS] Organization profile source is ready at .github/profile/README.md")

if __name__ == "__main__":
    sync_org_profile()
