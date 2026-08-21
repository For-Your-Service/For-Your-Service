# Databricks notebook source
# DBTITLE 1,AWS Setup Guide - For Your Service
# MAGIC %md
# MAGIC # AWS Quick Setup Guide - For Your Service
# MAGIC
# MAGIC **Organization:** 7 Eagle Group
# MAGIC **Account ID:** 342050998009
# MAGIC **Account Owner:** W. Free Hall (whall4.wh@gmail.com)
# MAGIC **Region:** us-east-1
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Mission
# MAGIC Set up secure AWS IAM credentials for the For Your Service veteran job matching platform.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📋 Prerequisites Checklist
# MAGIC
# MAGIC - [ ] AWS Account 342050998009 access
# MAGIC - [ ] Root account MFA enabled
# MAGIC - [ ] Password manager ready
# MAGIC - [ ] 15 minutes available
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🚀 Quick Start (5 Steps)
# MAGIC
# MAGIC ### Step 1: Create IAM User
# MAGIC Go to: https://console.aws.amazon.com/iam/home#/users
# MAGIC
# MAGIC 1. Click **"Add users"**
# MAGIC 2. Username: `foryourservice-app`
# MAGIC 3. AWS credential type: **Access key** (NOT console access needed)
# MAGIC 4. Click **"Next"**
# MAGIC
# MAGIC ### Step 2: Attach Custom Policy
# MAGIC 1. Select **"Attach policies directly"**
# MAGIC 2. Click **"Create policy"** (opens new tab)
# MAGIC 3. Switch to **JSON** tab
# MAGIC 4. Copy policy from **Cell 2** below
# MAGIC 5. Name: `ForYourServicePolicy`
# MAGIC 6. Create policy, return to user creation tab
# MAGIC 7. Refresh policies and select `ForYourServicePolicy`
# MAGIC 8. Click **"Next"**, then **"Create user"**
# MAGIC
# MAGIC ### Step 3: Create Access Keys
# MAGIC 1. Click on newly created user `foryourservice-app`
# MAGIC 2. Go to **"Security credentials"** tab
# MAGIC 3. Scroll to **"Access keys"** → Click **"Create access key"**
# MAGIC 4. Select: **"Application running outside AWS"**
# MAGIC 5. Description: `Databricks integration`
# MAGIC 6. Click **"Create access key"**
# MAGIC
# MAGIC ⚠️ **CRITICAL:** Copy both keys NOW (secret key shown only once)
# MAGIC
# MAGIC ### Step 4: Create Databricks Secret Scope
# MAGIC In Databricks:
# MAGIC
# MAGIC 1. Click your **username** (top-right) → **Settings**
# MAGIC 2. **Developer** → **Secrets**
# MAGIC 3. Click **"Create Scope"**
# MAGIC 4. Scope name: `aws-credentials`
# MAGIC 5. Click **"Create"**
# MAGIC
# MAGIC ### Step 5: Add Secrets
# MAGIC Add three secrets to `aws-credentials` scope:
# MAGIC
# MAGIC ```
# MAGIC Key: aws_access_key_id
# MAGIC Value: [Your Access Key ID - starts with AKIA...]
# MAGIC
# MAGIC Key: aws_secret_access_key
# MAGIC Value: [Your Secret Access Key - long alphanumeric string]
# MAGIC
# MAGIC Key: aws_region
# MAGIC Value: us-east-1
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Test Connection
# MAGIC
# MAGIC After completing all 5 steps, run **Cell 3** below to test your AWS connection.

# COMMAND ----------

