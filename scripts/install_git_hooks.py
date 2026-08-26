#!/usr/bin/env python3
"""
File: scripts/install_git_hooks.py
Description: Configures Git to use version-controlled .githooks/ directory
Author: Free Hall <whall4.wh@gmail.com>
"""

import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def install_hooks():
    root = Path(__file__).resolve().parent.parent
    githooks_dir = root / ".githooks"
    
    if not githooks_dir.exists():
        print(f"[-] .githooks directory not found at {githooks_dir}")
        sys.exit(1)
        
    print("[*] Setting git core.hooksPath to .githooks...")
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=str(root), check=True)
    print("[OK] Successfully installed Conventional Commits git hook guardrail.")

if __name__ == "__main__":
    install_hooks()
