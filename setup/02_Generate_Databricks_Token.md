# 🔐 Generate Databricks Personal Access Token

**For:** Hugging Face Spaces API Backend  
**Developer:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group  
**Date:** 2026-08-09

---

## Purpose

Generate a Personal Access Token (PAT) for the Hugging Face API backend to connect to Databricks Unity Catalog.

---

## Steps

### 1. Navigate to User Settings

1. Click your **email address** in the top-right corner
2. Select **"User Settings"**

### 2. Go to Developer Section

1. In the left sidebar, click **"Developer"**
2. Find the **"Access tokens"** section
3. Click **"Manage"**

### 3. Generate New Token

1. Click **"Generate new token"**
2. Configure:
   * **Comment:** `Hugging Face API Backend - For Your Service`
   * **Lifetime:** `90 days` (recommended)
3. Click **"Generate"**

### 4. Copy Token

**IMPORTANT:** The token is only shown ONCE!

1. Copy the token (starts with `dapi...`)
2. Store it securely (you'll need it for Hugging Face Spaces)

**Example format:**
```
dapi1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o
```

---

## Token Permissions

This token has access to:
* ✅ Unity Catalog tables (read/write)
* ✅ SQL Warehouse execution
* ✅ Databricks SQL Connector authentication

---

## Configure in Hugging Face

In your HF Space → **Settings** → **Variables and secrets**:

| Secret Name | Value |
|-------------|-------|
| `DATABRICKS_TOKEN` | `dapi...` (the token you just copied) |
| `DATABRICKS_SERVER_HOSTNAME` | `dbc-3e95d032-684c.cloud.databricks.com` |
| `DATABRICKS_HTTP_PATH` | Get from SQL Warehouse → Connection Details |

---

## Security Best Practices

* ✅ Use 90-day expiration (rotate regularly)
* ✅ Store in HF Spaces secrets (not in code)
* ✅ Never commit tokens to Git
* ✅ Revoke immediately if compromised

---

## Next Step

Once token is generated → [Configure Hugging Face Spaces](../huggingface/README.md)

