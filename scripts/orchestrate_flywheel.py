"""
Gunslinger Lore: The Ka-Tet Wheel - Master Orchestrator
Executes the full 5-stage loop in sequence:
Ingestion -> Transformation -> Test/Remediation -> Docs Synchronization.
"""
import subprocess
import sys
from pathlib import Path

# Resolve scripts dir dynamically across Windows and Linux
SCRIPTS_DIR = Path(__file__).resolve().parent

def run_stage(script_name: str, desc: str) -> bool:
    script_path = SCRIPTS_DIR / script_name
    print(f"\n==========================================")
    print(f"[Gunslinger] Initiating: {desc}")
    print(f"==========================================")
    
    if not script_path.exists():
        print(f"[Gunslinger] Target missing: {script_path}")
        return False

    res = subprocess.run([sys.executable, str(script_path)])
    return res.returncode == 0

def main():
    print("[Gunslinger] Turning the Wheel of Ka for 'For Your Service'...")
    
    # 1. Ingest Real-World Public Data
    run_stage("02_live_data_ingestor.py", "Stage 2: Live Real-World Data Ingestion")

    # 2. Run Test & Autonomous Remediation Battery
    run_stage("03_test_and_remediate.py", "Stage 3: Testing & Autonomous Remediation")

    # 3. Synchronize Architecture & Mermaid Documentation
    run_stage("04_sync_docs.py", "Stage 4: Architecture Docs & Mermaid Generation")

    print("\n[Gunslinger] The wheel has turned full circle. Ready on the line.")

if __name__ == "__main__":
    main()
