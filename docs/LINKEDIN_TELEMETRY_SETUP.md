# 📢 LinkedIn Live Telemetry Broadcast Setup Guide
## For Your Service — Veteran Career Transition Intelligence

**Lead Architect:** Free Hall <whall4.wh@gmail.com>
**Organization:** 7 Eagle Group
**Workflow:** [`.github/workflows/linkedin-broadcast.yml`](../.github/workflows/linkedin-broadcast.yml)
**Broadcast Script:** [`scripts/broadcast_linkedin_telemetry.py`](../scripts/broadcast_linkedin_telemetry.py)

---

## 🎯 Overview

This automated integration broadcasts daily system health, test suite pass rates, and platform impact metrics (visitors, matches run, recruiter intros) directly to your LinkedIn feed.

---

## 📋 2-Step Configuration

### Step 1: LinkedIn Developer Portal Registration
1. Visit the [LinkedIn Developer Portal](https://developer.linkedin.com).
2. Create / Select your application.
3. Under the **Products** tab, request access to:
   * **Share on LinkedIn** (Provides `w_member_social` permission)
   * **Sign In with LinkedIn using OpenID Connect** (Provides `openid`, `profile`, `email`)
4. Use the OAuth 2.0 Token Generator to generate a user access token with `w_member_social` scope.
5. Retrieve your member ID / Person URN via the `/v2/userinfo` endpoint.

---

### Step 2: Configure GitHub Repository Secrets
Navigate to your GitHub repository:
**Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret**:

| Secret Name | Description | Example Value |
| :--- | :--- | :--- |
| `LINKEDIN_ACCESS_TOKEN` | OAuth 2.0 User Access Token | `AQV...` |
| `LINKEDIN_PERSON_URN` | Unique LinkedIn Member ID | `urn:li:person:AbCdEf123` *(or raw ID `AbCdEf123`)* |

---

## 🚀 Execution & Schedule

* **Daily Automatic Trigger:** Runs every day at **`09:00 UTC`** via GitHub Actions.
* **Manual On-Demand Trigger:** Go to **Actions** ➔ **Daily LinkedIn Telemetry Broadcast** ➔ **Run workflow**.
* **Local Test / Dry-Run:**
  ```powershell
  python scripts/broadcast_linkedin_telemetry.py --dry-run
  ```

---

## 📊 Sample Output Broadcast

```text
🇺🇸 For Your Service — Veteran Career Transition Intelligence
Daily Telemetry & System Health Report (August 21, 2026):

🟢 System Status: 100% Operational
🧪 Automated Test Suite: 126 / 126 Passing (100% Integrity)
👥 Active Platform Visitors: 1,420+
⚡ AI Semantic Matches Run: 865+
🦅 7 Eagle Recruiter Intros: 218+

Bridging military experience with high-impact civilian opportunities.
🔗 Live Serverless Portal: https://fys-matching-app-7474643734871839.aws.databricksapps.com
💻 Open Source Architecture: https://github.com/For-Your-Service/For-Your-Service

#Veterans #MilitaryTransition #DevOps #CloudEngineering #Databricks #AI #7EagleGroup
```
