#!/usr/bin/env python3
"""
File: terraform/scripts/test_cloud_connectivity.py
Description: Multi-Cloud Pre-Flight Connectivity & Authentication Verifier
Lead Architect: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import sys
import json
import urllib.request
import urllib.error

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def test_aws():
    print_header("1. Testing AWS Authentication & Connectivity")
    try:
        import boto3
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS Connected: Account {identity.get('Account')}, ARN: {identity.get('Arn')}")
        return True
    except ImportError:
        print("⚠️  boto3 not installed in local environment (skipping live AWS call)")
        return None
    except Exception as e:
        print(f"❌ AWS Connection Error: {e}")
        return False

def test_gcp():
    print_header("2. Testing GCP Authentication & Connectivity")
    try:
        from google.auth import default
        credentials, project = default()
        print(f"✅ GCP Connected: Project {project}")
        return True
    except ImportError:
        print("⚠️  google-auth not installed in local environment (skipping live GCP call)")
        return None
    except Exception as e:
        print(f"❌ GCP Connection Error: {e}")
        return False

def test_databricks():
    print_header("3. Testing Databricks API Connectivity")
    host = os.getenv("DATABRICKS_SERVER_HOSTNAME", "dbc-3e95d032-684c.cloud.databricks.com")
    token = os.getenv("DATABRICKS_TOKEN", "")
    
    if not token:
        print("ℹ️  DATABRICKS_TOKEN not set in environment (skipping live request)")
        return None

    url = f"https://{host}/api/2.0/clusters/spark-versions"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f"✅ Databricks Connected to {host}")
                return True
    except Exception as e:
        print(f"❌ Databricks Connection Error: {e}")
        return False

def test_huggingface():
    print_header("4. Testing Hugging Face API Connectivity")
    url = "https://huggingface.co/api/spaces/For-Your-Service/fys-matching-api"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ForYourService-IaC-Verifier"})
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"✅ Hugging Face API reachable (HTTP {response.status})")
            return True
    except urllib.error.HTTPError as e:
        if e.code in [200, 404, 401]: # 404 or 401 still proves reachability
            print(f"✅ Hugging Face endpoint reachable (HTTP {e.code})")
            return True
        print(f"❌ Hugging Face HTTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Hugging Face Connection Error: {e}")
        return False

def main():
    print("================================================================")
    print(" For Your Service - Multi-Cloud Pre-Flight Connectivity Check")
    print("================================================================")
    
    results = {
        "AWS": test_aws(),
        "GCP": test_gcp(),
        "Databricks": test_databricks(),
        "Hugging Face": test_huggingface()
    }
    
    print_header("Summary of Pre-Flight Checks")
    for cloud, status in results.items():
        status_str = "✅ PASS" if status is True else ("⚠️  SKIPPED" if status is None else "❌ FAIL")
        print(f"  {cloud.ljust(15)}: {status_str}")

if __name__ == "__main__":
    main()
