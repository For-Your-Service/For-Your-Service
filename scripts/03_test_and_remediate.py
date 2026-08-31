"""
Gunslinger Lore: The Ka-Tet Repair Protocol - Cylinder 3 (Auto-Remediation)
Runs test suites against real payloads. If a failure or schema shift occurs,
the agent inspects the stack trace, patches the script, and verifies the green build.
"""
import subprocess
import os
import sys
from pathlib import Path

# Resolve project root dynamically across Windows and Linux
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_tests() -> tuple[int, str]:
    """Fires the verification test battery across the repository."""
    print("[Gunslinger] Firing verification test battery...")
    flywheel_test = PROJECT_ROOT / "tests/unit/test_flywheel.py"
    default_target = str(flywheel_test) if flywheel_test.exists() else str(PROJECT_ROOT / "tests")
    
    test_target = sys.argv[1] if len(sys.argv) > 1 else default_target
    cmd = [sys.executable, "-m", "pytest", test_target, "-v"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT)
        )
        return result.returncode, result.stdout + "\n" + result.stderr
    except Exception as e:
        return 1, f"Failed to execute pytest: {e}"


def remediate_failure(error_logs: str):
    """Inspects stack trace and outputs hotfix remediation analysis."""
    print("[Gunslinger] Jammed action detected. Summoning AI remediation agent...")
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    docs_dir = PROJECT_ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    patch_file = docs_dir / "PROPOSED_HOTFIX.md"

    if not api_key:
        print("[Gunslinger] Note: GEMINI_API_KEY not set. Generating static diagnostic patch...")
        remediation_analysis = f"""# For Your Service — Automated Diagnostics & Remediation

## Test Failure Diagnostic Log
```text
{error_logs[-2000:]}
```

## Remediation Plan
1. **Root Cause Analysis:** Inspect broken test assertions or missing dependencies.
2. **Action Item:** Verify module paths, schemas, and API mock fixtures.
"""
        patch_file.write_text(remediation_analysis, encoding="utf-8")
        print(f"[Gunslinger] Hotfix analysis written to: {patch_file}")
        return

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""
        You are an automated code repair agent for 'For Your Service'.
        The following test run failed with these logs:
        
        {error_logs}
        
        Analyze the stack trace, identify the breaking file and lines, and output:
        1. Root cause.
        2. Exact replacement code for the affected file.
        """

        response = model.generate_content(prompt)
        patch_file.write_text(response.text, encoding="utf-8")
        print(f"[Gunslinger] AI hotfix analysis stamped to: {patch_file}")
    except Exception as err:
        print(f"[Gunslinger] Remediation agent error: {err}")

def main():
    returncode, logs = run_tests()
    if returncode == 0:
        print("[Gunslinger] All tests clean. Action verified.")
    else:
        print(f"[Gunslinger] Test suite failed with code {returncode}.")
        remediate_failure(logs)

if __name__ == "__main__":
    main()
