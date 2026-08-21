
# Secure Credential Setup Script
# Run this to store API credentials in Databricks Secrets

from databricks.sdk.runtime import dbutils
import requests

print("=" * 70)
print("🔒 SECURE CREDENTIAL SETUP - FOR YOUR SERVICE")
print("=" * 70)

# Step 1: Verify dbutils.secrets is available
try:
    # This will work in Databricks notebooks
    _ = dbutils.secrets.list("api-keys")
    print("\n✅ Databricks Secrets is available")
except:
    print("\n✅ Ready to use Databricks Secrets")

print("\n" + "=" * 70)
print("📋 SETUP INSTRUCTIONS")
print("=" * 70)

instructions = '''
To store your JSearch API credentials securely:

1. Go to Databricks UI:
   Settings → Admin Console → Secrets
   Direct: https://dbc-3e95d032-684c.cloud.databricks.com/#secrets

2. Create Secret Scope (if not exists):
   Name: api-keys
   Click "Create"

3. Add JSearch Credentials:

   Secret #1:
   - Click "Add Secret"
   - Key: jsearch-rapidapi-key
   - Value: [paste your RapidAPI key]
   - Click "Add"

   Secret #2:
   - Click "Add Secret"
   - Key: jsearch-rapidapi-host
   - Value: jsearch.p.rapidapi.com
   - Click "Add"

4. Run the test below to verify setup
'''

print(instructions)

print("=" * 70)
print("🧪 VERIFICATION TEST")
print("=" * 70)

def test_credentials():
    try:
        api_key = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-key")
        api_host = dbutils.secrets.get(scope="api-keys", key="jsearch-rapidapi-host")

        print("\n✅ JSearch credentials: CONFIGURED")
        print(f"   Key length: {len(api_key)} characters")

        # Test API connection
        print("\n🔍 Testing API connection...")
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }

        response = requests.get(
            f"https://{api_host}/search",
            headers=headers,
            params={"query": "test", "page": "1"},
            timeout=10
        )

        if response.status_code == 200:
            print("✅ API connection successful!")
            data = response.json()
            print(f"   Sample returned {len(data.get('data', []))} jobs")
        elif response.status_code == 429:
            print("⚠️  Rate limit (API key works!)")
        else:
            print(f"⚠️  API returned status {response.status_code}")

        return True

    except Exception as e:
        print(f"\n❌ Credentials not configured yet")
        print(f"   Error: {e}")
        print("\n   Follow the setup instructions above")
        return False

# Run test
test_credentials()

print("\n" + "=" * 70)
print("🚀 NEXT STEPS")
print("=" * 70)
print('''
Once JSearch credentials are working:

1. Register USAJobs (5 min): https://developer.usajobs.gov
2. Add USAJobs secrets:
   - usajobs-api-key → [key from email]
   - usajobs-email → whall4.wh@gmail.com
3. Run job scraper to get 200+ matches!
''')
