#!/usr/bin/env python3
"""
File: scripts/generate_ai_summary.py
Description: Intelligent Narrative Engineering Summary Generator for LinkedIn & Stakeholders
Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
METRICS_FILE = ROOT_DIR / "data" / "analytics" / "usage_metrics.json"

def get_platform_metrics():
    today_str = datetime.now().strftime("%Y-%m-%d")
    metrics = {
        "metric_date": today_str,
        "total_visitors": 1420,
        "total_matches_run": 865,
        "veterans_connected": 218
    }
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                saved_date = saved.get("metric_date") or saved.get("date")
                if saved_date == today_str:
                    metrics["total_visitors"] = int(saved.get("total_visitors", 1420))
                    metrics["total_matches_run"] = int(saved.get("total_matches_run", 865))
                    metrics["veterans_connected"] = int(saved.get("veterans_connected", 218))
        except Exception:
            pass
    return metrics

def build_narrative_post():
    metrics = get_platform_metrics()
    now_date = datetime.now().strftime("%B %d, %Y")

    narrative = (
        f"Every transition from the military generates thousands of operational data points—leadership tours, classified clearances, technical MOS codes, and crisis-tested decision-making.\n\n"
        f"The problem? Traditional civilian applicant tracking systems (ATS) still struggle to read military records, and transitioning service members are often left translating their own resumes by hand.\n\n"
        f"Over the past few weeks with 7 Eagle Group, we've been building For Your Service—an enterprise AI platform designed to turn service data into real-world career trajectory for veterans, at zero cost to the service member.\n\n"
        f"---\n\n"
        f"🛠️ Dual-Environment Workflow: PowerShell + Native Omarchy Bash\n"
        f"Modern distributed engineering requires flexibility across operating systems and toolchains:\n"
        f"• Windows Control Center (PowerShell): High-level orchestration, cloud API automation, and infrastructure planning.\n"
        f"• Omarchy Linux (Native Arch Linux on ASUS ROG Flow Z13): Connected over encrypted SSH tunnels, running low-latency bash scripts, local PySpark feature transformations, and live Wayland desktop telemetry.\n"
        f"• Agentic Pair Programming: Deployed and orchestrated native instances of Google Antigravity (agy) across both systems, using autonomous AI agents to manage system diagnostics, package validation, and multi-commit provenance tracking directly from the CLI.\n\n"
        f"---\n\n"
        f"⚙️ The Cloud-Native & Lakehouse Architecture ($0 Cost Model)\n"
        f"Building high-impact software doesn't require burning thousands in cloud overhead:\n"
        f"1. Databricks Serverless Lakehouse: Deployed our veteran matching portal on Databricks Apps with Unity Catalog governance and Bronze ➔ Silver ➔ Gold Medallion architecture—configured to auto-suspend when idle for a $0 run-rate.\n"
        f"2. Local Neural Vector Search: 384-dimensional dense semantic tensor matching running locally in memory (all-MiniLM-L6-v2) without recurring third-party API costs.\n"
        f"3. Containerized Microservices: 4 slim Docker multi-stage containers published to ghcr.io (portal, api, ingestor, spark-runner).\n"
        f"4. Zero-Trust Infrastructure: Parameterized Helm 3 charts with Istio Service Mesh (strict mTLS, Canary 90/10 traffic splitting) and declarative Terraform IaC.\n\n"
        f"---\n\n"
        f"🇺🇸 What This Delivers to Transitioning Service Members:\n"
        f"• 'Combat-to-Code' Jargon De-Militarizer: Instantly translates NCOER/OER service bullets into quantified corporate impact statements that hiring managers understand.\n"
        f"• Clearance Fast-Track ROI: Calculates the strategic value of active Secret and TS/SCI clearances to bypass 18-month civilian onboarding backlogs.\n"
        f"• 100% Free Veteran Funding Links: Connects veterans directly to fully-funded certification programs (Onward to Opportunity / Syracuse IVMF, DoD COOL, ArmyIgnitED, and DoD SkillBridge).\n"
        f"• Live Verified Job Feeds: Direct indexing across federal defense contractors (Lockheed Martin, RTX, Northrop Grumman, General Dynamics, Boeing) and USAJOBS.\n\n"
        f"---\n\n"
        f"From Special Forces operations to enterprise cloud architecture, the mission remains the same: lead from the front, eliminate friction, and build systems that take care of our people.\n\n"
        f"Check out the live Databricks deployment or reach out if you're a transitioning veteran looking for your next mission.\n\n"
        f"👉 GitHub: https://github.com/For-Your-Service/For-Your-Service\n"
        f"👉 Live App: https://fys-matching-app-7474643734871839.aws.databricksapps.com\n\n"
        f"#Veterans #MilitaryTransition #Databricks #CloudEngineering #DevSecOps #Kubernetes #Docker #Terraform #ArchLinux #AI #Cybersecurity #SpecialForces #7EagleGroup #ForYourService"
    )
    return narrative

if __name__ == "__main__":
    print(build_narrative_post())
