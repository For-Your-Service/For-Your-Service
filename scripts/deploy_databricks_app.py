#!/usr/bin/env python3
"""
File: scripts/deploy_databricks_app.py
Description: Automated Databricks Apps Deployer for For Your Service (fys-matching-app)
Lead Architect: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
from pathlib import Path
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import apps

APP_NAME = "fys-matching-app"
DEFAULT_HOST = "https://dbc-3e95d032-684c.cloud.databricks.com"
APP_DIR = Path(__file__).resolve().parent.parent / "app"

def deploy_app():
    print("=================================================================")
    print(f" Deploying {APP_NAME} to Databricks Apps")
    print("=================================================================")
    
    host = os.getenv("DATABRICKS_SERVER_HOSTNAME", os.getenv("DATABRICKS_HOST", DEFAULT_HOST))
    if not host.startswith("https://"):
        host = f"https://{host}"
        
    token = os.getenv("DATABRICKS_TOKEN")
    
    if not token:
        print("\n[!] DATABRICKS_TOKEN environment variable is required.")
        print(f"    Target Workspace: {host}")
        print("    Please set DATABRICKS_TOKEN before running:")
        print("      $env:DATABRICKS_TOKEN=\"dapi...\"")
        print("      $env:DATABRICKS_HOST=\"" + host + "\"")
        sys.exit(1)

    print(f"[*] Authenticating with workspace: {host}...")
    w = WorkspaceClient(host=host, token=token)
    user = w.current_user.me().user_name
    print(f"[✓] Authenticated as: {user}")

    # Check if app already exists
    print(f"[*] Checking status of app '{APP_NAME}'...")
    try:
        app_obj = w.apps.get(name=APP_NAME)
        print(f"[✓] Found existing app '{APP_NAME}' (Status: {app_obj.status.state})")
    except Exception:
        print(f"[*] App '{APP_NAME}' not found. Creating new Databricks App...")
        app_obj = w.apps.create_and_wait(
            app=apps.App(
                name=APP_NAME,
                spec=apps.AppSpec(
                    description="For Your Service - AI Veteran Job Matching Portal (7 Eagle Group)"
                )
            )
        )
        print(f"[✓] Created app '{APP_NAME}'")

    print(f"[*] Source directory: {APP_DIR}")
    print("[*] Deploying code and syncing app.yaml environment variables...")
    
    # Deploy app
    deployment = w.apps.deploy_and_wait(
        app_name=APP_NAME,
        app_deployment=apps.AppDeployment(
            source_code_path=str(APP_DIR)
        )
    )
    
    print(f"[✓] Deployment succeeded: {deployment.deployment_id}")
    
    # Retrieve updated app info
    final_app = w.apps.get(name=APP_NAME)
    print("\n=================================================================")
    print(f" [SUCCESS] App '{APP_NAME}' is LIVE!")
    print(f" URL:    {final_app.url}")
    print(f" Status: {final_app.status.state}")
    print("=================================================================")

if __name__ == "__main__":
    deploy_app()
