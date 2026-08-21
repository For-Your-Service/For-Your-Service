#!/usr/bin/env python3
"""
File: scripts/deploy_databricks_app.py
Description: Automated Databricks Apps Deployer for For Your Service (fys-matching-app)
Lead Architect: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
import base64
from pathlib import Path
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import apps, workspace

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
    print(f"[OK] Authenticated as: {user}")

    ws_import_dir = f"/Users/{user}/apps/{APP_NAME}"
    ws_source_path = f"/Workspace/Users/{user}/apps/{APP_NAME}"
    print(f"[*] Target workspace directory: {ws_import_dir}")
    w.workspace.mkdirs(ws_import_dir)

    # Upload all files in app/
    print("[*] Uploading application files to workspace...")
    for file_path in APP_DIR.glob("*"):
        if file_path.is_file() and not file_path.name.endswith(".pyc"):
            target_ws_path = f"{ws_import_dir}/{file_path.name}"
            with open(file_path, "rb") as f:
                b64_content = base64.b64encode(f.read()).decode("utf-8")
            w.workspace.import_(
                path=target_ws_path,
                content=b64_content,
                format=workspace.ImportFormat.AUTO,
                overwrite=True
            )
            print(f"  -> Uploaded: {file_path.name}")

    # Check if app already exists
    print(f"[*] Checking status of app '{APP_NAME}'...")
    try:
        app_obj = w.apps.get(name=APP_NAME)
        print(f"[OK] Found existing app '{APP_NAME}'")
    except Exception:
        print(f"[*] App '{APP_NAME}' not found. Creating new Databricks App...")
        app_obj = w.apps.create_and_wait(
            app=apps.App(
                name=APP_NAME,
                description="For Your Service - AI Veteran Job Matching Portal (7 Eagle Group)",
                default_source_code_path=ws_source_path
            )
        )
        print(f"[OK] Created app '{APP_NAME}'")

    print("[*] Deploying code and syncing app.yaml environment variables...")

    # Deploy app
    deployment = w.apps.deploy_and_wait(
        app_name=APP_NAME,
        app_deployment=apps.AppDeployment(
            source_code_path=ws_source_path
        )
    )

    print(f"[OK] Deployment completed: {deployment.deployment_id}")

    # Retrieve updated app info
    final_app = w.apps.get(name=APP_NAME)
    print("\n=================================================================")
    print(f" [SUCCESS] App '{APP_NAME}' is LIVE!")
    print(f" URL:    {final_app.url}")
    print(f" Status: {final_app.compute_status.state if final_app.compute_status else 'UNKNOWN'}")
    print("=================================================================")

if __name__ == "__main__":
    deploy_app()
