# Databricks Ingestion Script for 7 Eagle Group API

# 1. Define and retrieve widget parameters passed from GitHub Actions
dbutils.widgets.text("seven_eagle_id", "", "7 Eagle App ID")
dbutils.widgets.text("seven_eagle_key", "", "7 Eagle App Key")

seven_eagle_id = dbutils.widgets.get("seven_eagle_id")
seven_eagle_key = dbutils.widgets.get("seven_eagle_key")

if not seven_eagle_id or not seven_eagle_key:
    raise ValueError("Missing 7 Eagle Group API credentials from job parameters.")

# 2. Build HTTP Headers
headers = {
    "X-App-Id": seven_eagle_id,
    "X-App-Key": seven_eagle_key,
    "Content-Type": "application/json",
}

print(f"Loaded credentials for 7 Eagle App ID: {seven_eagle_id[:4]}****")
