# AWS IAM Security Setup - For Your Service

**Organization:** 7 Eagle Group
**Account ID:** 342050998009
**Account Owner:** W. Free Hall
**Region:** us-east-1 (Free Tier Optimized)
**Date:** 2026-08-13

## Overview

Secure AWS IAM configuration for the For Your Service veteran job matching platform, following least privilege access principles and optimized for AWS Free Tier usage.

## Security Principles

✅ **Least Privilege Access** - Only grant permissions needed
✅ **No Root Account Usage** - Create IAM users instead
✅ **MFA Enabled** - Multi-factor authentication on all accounts
✅ **Access Key Rotation** - Regular credential updates
✅ **Audit Logging** - Track all AWS actions via CloudTrail

---

## Step 1: Secure Root Account

🚨 **CRITICAL:** Root account (whall4.wh+aws1@gmail.com) should NEVER be used for day-to-day operations.

### Actions:
1. Enable MFA on root account
2. Use virtual MFA device (Google Authenticator or Authy)
3. Store recovery codes securely
4. Log out and do not use root account again

**URL:** https://console.aws.amazon.com/iam/home#/security_credentials

---

## Step 2: Create IAM User

### User Details:
- **Username:** `foryourservice-app`
- **Console Access:** Optional (for debugging)
- **Password:** Custom (stored in password manager)
- **Password Reset:** Not required

**URL:** https://console.aws.amazon.com/iam/home#/users

---

## Step 3: Custom IAM Policy (Recommended)

### Policy Name: `ForYourServicePolicy`

This policy implements least privilege access, scoped specifically to For Your Service resources.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3ForYourServiceBuckets",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::foryourservice-*",
        "arn:aws:s3:::foryourservice-*/*"
      ]
    },
    {
      "Sid": "DynamoDBForYourService",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:342050998009:table/foryourservice-*"
    },
    {
      "Sid": "LambdaForYourService",
      "Effect": "Allow",
      "Action": [
        "lambda:InvokeFunction",
        "lambda:GetFunction",
        "lambda:ListFunctions"
      ],
      "Resource": "arn:aws:lambda:us-east-1:342050998009:function:foryourservice-*"
    },
    {
      "Sid": "CloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogStreams"
      ],
      "Resource": "arn:aws:logs:us-east-1:342050998009:log-group:/aws/lambda/foryourservice-*"
    },
    {
      "Sid": "SecretsManagerAccess",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:342050998009:secret:foryourservice/*"
    }
  ]
}
```

### Policy Scope:
- **S3:** Only buckets prefixed with `foryourservice-*`
- **DynamoDB:** Only tables prefixed with `foryourservice-*`
- **Lambda:** Only functions prefixed with `foryourservice-*`
- **CloudWatch:** Logging only for Lambda functions
- **Secrets Manager:** Only secrets under `foryourservice/` path

---

## Step 4: Create Access Keys

### Process:
1. Navigate to IAM → Users → foryourservice-app
2. Security credentials tab → Create access key
3. Use case: "Application running outside AWS"
4. Description: "Databricks integration for For Your Service"

### Credentials to Store:
- **Access Key ID:** Starts with `AKIA...`
- **Secret Access Key:** Shown only once - store immediately

⚠️ **SECURITY:** Store in password manager and Databricks Secrets (never in code)

---

## Step 5: Databricks Secrets Integration

### Secret Scope: `aws-credentials`

Store the following secrets in Databricks:

| Secret Key | Value | Description |
|------------|-------|-------------|
| `aws_access_key_id` | `AKIA...` | IAM user access key |
| `aws_secret_access_key` | `********` | IAM user secret key |
| `aws_region` | `us-east-1` | Primary AWS region |
| `aws_account_id` | `342050998009` | AWS account number |

### Usage in Databricks:
```python
import boto3

# Retrieve credentials securely
aws_key = dbutils.secrets.get(scope="aws-credentials", key="aws_access_key_id")
aws_secret = dbutils.secrets.get(scope="aws-credentials", key="aws_secret_access_key")
aws_region = dbutils.secrets.get(scope="aws-credentials", key="aws_region")

# Create AWS client
s3_client = boto3.client('s3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=aws_region
)

# Configure Spark for S3
spark.conf.set("fs.s3a.access.key", aws_key)
spark.conf.set("fs.s3a.secret.key", aws_secret)
spark.conf.set("fs.s3a.endpoint", f"s3.{aws_region}.amazonaws.com")
```

---

## Step 6: AWS Budget Alerts

### Configuration:
- **Budget Type:** Zero spend budget
- **Name:** `ForYourService-FreeTier-Alert`
- **Alert Email:** whall4.wh@gmail.com
- **Threshold:** $0.00 (alert on ANY charges)

**URL:** https://console.aws.amazon.com/billing/home#/budgets

---

## Step 7: Optional - MFA on IAM User

For additional security, enable MFA on the `foryourservice-app` IAM user:

1. IAM → Users → foryourservice-app → Security credentials
2. Assign MFA device → Authenticator app
3. Device name: `foryourservice-app-mfa`
4. Scan QR code and enter two consecutive codes

---

## AWS Free Tier Limits

Stay within these limits to maintain $0 monthly costs:

| Service | Free Tier Limit | Usage Pattern |
|---------|----------------|---------------|
| **S3** | 5 GB storage, 20K GET, 2K PUT | Resume storage, model weights |
| **Lambda** | 1M requests/month, 400K GB-sec | API endpoints |
| **DynamoDB** | 25 GB storage, 25 RCU/WCU | Veteran/job profiles |
| **EC2** | 750 hours/month (t2.micro) | Optional Kubernetes control |
| **CloudWatch** | 10 custom metrics, 5 GB logs | Monitoring |

---

## Resource Naming Convention

All AWS resources for this project use the prefix `foryourservice-` for:
- Easy identification
- Policy scoping
- Cost tracking
- Security isolation

**Examples:**
- S3 Bucket: `foryourservice-resumes-prod`
- DynamoDB Table: `foryourservice-veterans`
- Lambda Function: `foryourservice-match-api`
- CloudWatch Log: `/aws/lambda/foryourservice-match-api`

---

## Security Checklist

- [ ] Root account MFA enabled
- [ ] Root account NOT used for operations
- [ ] IAM user `foryourservice-app` created
- [ ] Custom `ForYourServicePolicy` attached
- [ ] Access keys created and stored securely
- [ ] Secrets stored in Databricks (scope: `aws-credentials`)
- [ ] Budget alerts configured ($0 threshold)
- [ ] IAM user MFA enabled (optional but recommended)
- [ ] Resource naming convention documented
- [ ] Connection tested from Databricks

---

## Next Steps

1. **Test Connection:** Verify IAM credentials work from Databricks
2. **Create S3 Bucket:** `foryourservice-data-prod` in us-east-1
3. **Create DynamoDB Tables:**
   - `foryourservice-veterans`
   - `foryourservice-jobs`
4. **Deploy Lambda Functions:** API endpoints for matching
5. **Set Up Monitoring:** CloudWatch dashboards and alarms

---

## References

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Free Tier Details](https://aws.amazon.com/free/)
- [Databricks AWS Integration](https://docs.databricks.com/aws/index.html)
- [For Your Service GitHub](https://github.com/For-Your-Service/For-Your-Service)

---

**Last Updated:** 2026-08-13
**Maintained By:** Free Hall (whall4.wh@gmail.com)
**Organization:** 7 Eagle Group
