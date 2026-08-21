#!/usr/bin/env python3
"""
File: scripts/broadcast_linkedin_update.py
Description: Wrapper / Entrypoint for Automated LinkedIn Telemetry Broadcast
Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    from scripts.broadcast_linkedin_telemetry import broadcast_to_linkedin
except ImportError:
    from broadcast_linkedin_telemetry import broadcast_to_linkedin

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    broadcast_to_linkedin(dry_run=is_dry)
