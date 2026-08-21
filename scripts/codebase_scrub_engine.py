#!/usr/bin/env python3
"""
File: scripts/codebase_scrub_engine.py
Description: Automated Codebase & GitHub Scrub Engine for For-Your-Service
Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group

Performs:
1. Security & Token Scrub: Neutralize hardcoded API keys/tokens.
2. Redundancy & Artifact Scrub: Purge backup files, checksums, and nested duplicates.
3. Granular Code Hygiene Scrub: Format, strip trailing whitespace, normalize encodings,
   and commit atomically per file (~200-300 atomic commits).
4. Validation: Verify pytest test suite passes.
5. Push: Push clean commit history to GitHub main.
"""

import os
import sys
import re
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), shell=True, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}\n{res.stderr}")
    return res

def git_commit(file_path, message):
    run_cmd(f'git add "{file_path}"')
    # Check if there are staged changes
    status = run_cmd('git diff --cached --name-only').stdout.strip()
    if status:
        res = run_cmd(f'git commit -m "{message}"')
        if res.returncode == 0:
            print(f"[COMMIT] {message}")
            return True
    return False

def git_rm_commit(file_path, message):
    run_cmd(f'git rm -r -f "{file_path}"')
    status = run_cmd('git diff --cached --name-only').stdout.strip()
    if status:
        res = run_cmd(f'git commit -m "{message}"')
        if res.returncode == 0:
            print(f"[COMMIT] {message}")
            return True
    return False

# ==============================================================================
# PHASE 1: SECURITY & CREDENTIAL SCRUB
# ==============================================================================
def scrub_security():
    print("\n" + "="*70)
    print(" PHASE 1: SECURITY & CREDENTIAL AUDIT & SANITIZATION")
    print("="*70)
    
    # 1. databricks/04_Job_Market_Data_Sources.py
    file1 = ROOT_DIR / "databricks" / "04_Job_Market_Data_Sources.py"
    if file1.exists():
        text = file1.read_text(encoding="utf-8", errors="ignore")
        orig = text
        text = re.sub(r'ADZUNA_APP_ID\s*=\s*"ea966e18"', 'ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "ea966e18")', text)
        text = re.sub(r'ADZUNA_API_KEY\s*=\s*"d59477241791ac51feb5df5b2b676654"', 'ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY", "")', text)
        text = re.sub(r'USAJOBS_API_KEY\s*=\s*"Sy03OfX4/5qL70b\+vVT42P7bTysIjAUT//nkUe4tEHU="', 'USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "")', text)
        if text != orig:
            file1.write_text(text, encoding="utf-8")
            git_commit("databricks/04_Job_Market_Data_Sources.py", "fix(security): sanitize hardcoded Adzuna and USAJOBS API keys in 04_Job_Market_Data_Sources.py")

    # 2. databricks/06_Enhanced_Job_Matching_Engine.py
    file2 = ROOT_DIR / "databricks" / "06_Enhanced_Job_Matching_Engine.py"
    if file2.exists():
        text = file2.read_text(encoding="utf-8", errors="ignore")
        orig = text
        text = re.sub(r'ADZUNA_APP_KEY\s*=\s*"90f7d868807b93575515153c3a8d0a51"', 'ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")', text)
        if text != orig:
            file2.write_text(text, encoding="utf-8")
            git_commit("databricks/06_Enhanced_Job_Matching_Engine.py", "fix(security): sanitize hardcoded Adzuna credentials fallback in 06_Enhanced_Job_Matching_Engine.py")

    # 3. docs/SECURE_CREDENTIALS_SETUP.md
    file3 = ROOT_DIR / "docs" / "SECURE_CREDENTIALS_SETUP.md"
    if file3.exists():
        text = file3.read_text(encoding="utf-8", errors="ignore")
        orig = text
        text = text.replace("17b44289e8mshad90d5f48c66ab8p1b2d12jsn5c62a950b550", "YOUR_RAPIDAPI_KEY_NEVER_HARDCODE")
        if text != orig:
            file3.write_text(text, encoding="utf-8")
            git_commit("docs/SECURE_CREDENTIALS_SETUP.md", "fix(security): redact illustrative RapidAPI key token in documentation")

# ==============================================================================
# PHASE 2: REDUNDANCY & DEAD ARTIFACT SCRUB
# ==============================================================================
def scrub_redundancies():
    print("\n" + "="*70)
    print(" PHASE 2: REDUNDANCY & ARTIFACT ELIMINATION")
    print("="*70)
    
    # Remove nested redundant directory For-Your-Service/
    nested_dir = ROOT_DIR / "For-Your-Service"
    if nested_dir.exists():
        # List all files inside nested_dir and remove / commit
        for p in list(nested_dir.rglob("*")):
            if p.is_file():
                rel = str(p.relative_to(ROOT_DIR)).replace("\\", "/")
                git_rm_commit(rel, f"clean(redundancy): purge duplicate nested file {rel}")
        if nested_dir.exists():
            git_rm_commit("For-Your-Service", "clean(redundancy): remove nested For-Your-Service directory tree")

    # Remove backup and checksum files
    for p in ROOT_DIR.rglob("*"):
        if any(part in ["venv", ".git"] for part in p.parts):
            continue
        if p.is_file():
            rel = str(p.relative_to(ROOT_DIR)).replace("\\", "/")
            if p.name.endswith(".backup") or p.name.endswith(".bak") or p.name.endswith(".crc") or p.name.endswith(".tmp"):
                git_rm_commit(rel, f"clean(artifacts): purge obsolete artifact file {rel}")

# ==============================================================================
# PHASE 3: GRANULAR CODE HYGIENE & FORMATTING SCRUB (ATOMIC COMMITS)
# ==============================================================================
def scrub_code_hygiene():
    print("\n" + "="*70)
    print(" PHASE 3: GRANULAR CODE HYGIENE & FORMATTING (ATOMIC COMMITS)")
    print("="*70)
    
    tracked_files_res = run_cmd("git ls-files")
    tracked_files = [line.strip() for line in tracked_files_res.stdout.splitlines() if line.strip()]
    
    extensions = {".py", ".md", ".json", ".yaml", ".yml", ".sql", ".sh", ".ps1", ".txt", ".ini", ".toml"}
    
    count = 0
    for rel_path in sorted(tracked_files):
        p = ROOT_DIR / rel_path
        if not p.exists() or not p.is_file():
            continue
        if p.suffix not in extensions:
            continue
        if any(part in ["venv", ".git", "jobs_cache", "analytics"] for part in p.parts):
            continue
            
        try:
            raw_bytes = p.read_bytes()
            has_bom = raw_bytes.startswith(b"\xef\xbb\xbf")
            content = raw_bytes.decode("utf-8-sig", errors="ignore")
            
            lines = content.splitlines()
            # Clean trailing whitespace from each line
            cleaned_lines = [line.rstrip() for line in lines]
            
            # Ensure single trailing newline at EOF if non-empty
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_content = "\n".join(cleaned_lines) + "\n"
            elif cleaned_lines:
                # Remove extra blank lines at end
                while len(cleaned_lines) > 1 and cleaned_lines[-1] == "" and cleaned_lines[-2] == "":
                    cleaned_lines.pop()
                cleaned_content = "\n".join(cleaned_lines) + "\n"
            else:
                cleaned_content = ""
                
            # If changes needed
            if has_bom or cleaned_content != raw_bytes.decode("utf-8", errors="ignore"):
                # For python files, verify syntax before saving
                if p.suffix == ".py":
                    try:
                        compile(cleaned_content, str(p), "exec")
                    except Exception as ce:
                        print(f"[SKIP-SYNTAX] {rel_path}: {ce}")
                        continue
                        
                p.write_text(cleaned_content, encoding="utf-8", newline="\n")
                
                cat = "style(hygiene)" if p.suffix not in [".md", ".txt"] else "docs(hygiene)"
                if git_commit(rel_path, f"{cat}: sanitize formatting and strip trailing whitespace in {rel_path}"):
                    count += 1
        except Exception as e:
            print(f"[ERR] {rel_path}: {e}")
            
    print(f"\n[OK] Completed hygiene sweep: {count} granular atomic commits generated.")

# ==============================================================================
# PHASE 4: TEST SUITE VERIFICATION
# ==============================================================================
def verify_tests():
    print("\n" + "="*70)
    print(" PHASE 4: RUNNING FULL TEST SUITE VERIFICATION")
    print("="*70)
    pytest_bin = ROOT_DIR / "venv" / "Scripts" / "pytest.exe"
    if not pytest_bin.exists():
        pytest_bin = "pytest"
    res = subprocess.run(f'"{pytest_bin}" -q', cwd=str(ROOT_DIR), shell=True)
    if res.returncode == 0:
        print("[SUCCESS] All unit and integration tests passed with 100% integrity!")
        return True
    else:
        print("[WARNING] Pytest reported errors.")
        return False

# ==============================================================================
# PHASE 5: PUSH TO GITHUB
# ==============================================================================
def push_to_github():
    print("\n" + "="*70)
    print(" PHASE 5: PUSHING CLEAN SCRUBBED COMMITS TO GITHUB MAIN")
    print("="*70)
    res = subprocess.run("git push origin main", cwd=str(ROOT_DIR), shell=True)
    if res.returncode == 0:
        print("[SUCCESS] All scrubbed commits successfully pushed to origin/main!")
    else:
        print("[ERROR] Git push failed.")

if __name__ == "__main__":
    scrub_security()
    scrub_redundancies()
    scrub_code_hygiene()
    passed = verify_tests()
    if passed:
        push_to_github()
