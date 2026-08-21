#!/usr/bin/env python3
"""
File: scripts/setup_databricks_secrets.py
Description: Securely manage and store API credentials in Databricks Secret Scopes
Lead Architect: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
from databricks.sdk import WorkspaceClient

DEFAULT_HOST = "https://dbc-3e95d032-684c.cloud.databricks.com"
SCOPE_NAME = "api-keys"

def sync_secrets():
    print("=================================================================")
    print(" Databricks Secret Scope Manager - For Your Service")
    print("=================================================================")

    host = os.getenv("DATABRICKS_HOST", os.getenv("DATABRICKS_SERVER_HOSTNAME", DEFAULT_HOST))
    token = os.getenv("DATABRICKS_TOKEN")

    if not token:
        print("[!] Error: DATABRICKS_TOKEN environment variable is required.")
        sys.exit(1)

    w = WorkspaceClient(host=host, token=token)
    print(f"[OK] Authenticated to {host} as {w.current_user.me().user_name}")

    # Ensure scope exists
    existing_scopes = [s.name for s in w.secrets.list_scopes()]
    if SCOPE_NAME not in existing_scopes:
        print(f"[*] Creating secret scope '{SCOPE_NAME}'...")
        w.secrets.create_scope(scope=SCOPE_NAME)
        print(f"[OK] Created scope '{SCOPE_NAME}'")
    else:
        print(f"[OK] Scope '{SCOPE_NAME}' exists")

    # Store USAJOBS Key if present in environment
    usajobs_key = os.getenv("USAJOBS_API_KEY")
    usajobs_email = os.getenv("USAJOBS_EMAIL", "whall4.wh@gmail.com")

    if usajobs_key:
        w.secrets.put_secret(scope=SCOPE_NAME, key="usajobs-api-key", string_value=usajobs_key)
        w.secrets.put_secret(scope=SCOPE_NAME, key="usajobs-email", string_value=usajobs_email)
        print("[OK] Encrypted & stored 'usajobs-api-key' in Databricks Secret Scope")
        print("[OK] Stored 'usajobs-email' in Databricks Secret Scope")

    # List all keys in scope (names only, values remain encrypted)
    print(f"\n[*] Current encrypted secrets in scope '{SCOPE_NAME}':")
    secrets = list(w.secrets.list_secrets(SCOPE_NAME))
    for s in secrets:
        print(f"  - {s.key} (Encrypted via KMS)")

    print("\n=================================================================")
    print(" In Databricks Notebooks & Workflows, retrieve securely using:")
    print(f'   api_key = dbutils.secrets.get(scope="{SCOPE_NAME}", key="usajobs-api-key")')
    print("=================================================================")

if __name__ == "__main__":
    sync_secrets()
