"""
AWS Connection Test Script
For Your Service - 7 Eagle Group
Tests IAM credentials stored in Databricks Secrets
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def test_aws_connection():
    """Test AWS connection using Databricks Secrets"""

    print("=" * 80)
    print("AWS CONNECTION TEST - For Your Service")
    print("Account: 342050098009 (W. Free Hall)")
    print("=" * 80)

    try:
        # Retrieve credentials from Databricks Secrets
        aws_key = dbutils.secrets.get(scope="aws-credentials", key="aws_access_key_id")
        aws_secret = dbutils.secrets.get(scope="aws-credentials", key="aws_secret_access_key")
        aws_region = dbutils.secrets.get(scope="aws-credentials", key="aws_region")

        print("\n✅ Credentials retrieved from Databricks Secrets")

        # Test STS (verify credentials)
        sts = boto3.client(
            "sts",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region,
        )

        identity = sts.get_caller_identity()

        print("\n🔌 AWS Connection SUCCESSFUL!")
        print(f"\n📊 Account Details:")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        print(f"   Region: {aws_region}")

        # Verify correct account
        expected_account = "342050998009"
        if identity["Account"] == expected_account:
            print(f"\n✅ Confirmed: Connected to correct account ({expected_account})")
        else:
            print(f"\n⚠️  WARNING: Connected to {identity['Account']}, expected {expected_account}")
            return False

        # Test S3 access
        print("\n📦 Testing S3 Access...")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region,
        )

        buckets = s3.list_buckets()
        bucket_count = len(buckets.get("Buckets", []))
        print(f"   Found {bucket_count} S3 bucket(s)")

        for bucket in buckets.get("Buckets", []):
            print(f"   - {bucket['Name']}")

        # Test DynamoDB access
        print("\n📊 Testing DynamoDB Access...")
        dynamodb = boto3.client(
            "dynamodb",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region,
        )

        tables = dynamodb.list_tables()
        table_count = len(tables.get("TableNames", []))
        print(f"   Found {table_count} DynamoDB table(s)")

        for table in tables.get("TableNames", []):
            print(f"   - {table}")

        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED - AWS Integration Ready!")
        print("=" * 80)

        return True

    except NoCredentialsError:
        print("\n❌ ERROR: No credentials found")
        print("   Make sure secrets are configured in 'aws-credentials' scope")
        return False

    except ClientError as e:
        print(f"\n❌ AWS ERROR: {e}")
        return False

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False


# Run test
if __name__ == "__main__":
    success = test_aws_connection()
    if not success:
        print("\n⚠️  Setup Instructions:")
        print("   1. Go to Settings → Developer → Secrets")
        print("   2. Create scope: aws-credentials")
        print("   3. Add secrets: aws_access_key_id, aws_secret_access_key, aws_region")
        print("   4. See docs/aws/AWS_IAM_SECURITY_SETUP.md for details")
