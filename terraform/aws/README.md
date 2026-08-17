# AWS Infrastructure for For Your Service

**Organization:** 7 Eagle Group  
**Project:** For Your Service - Veteran Job Matching Platform  
**Maintainer:** Free Hall (whall4.wh@gmail.com)

## Overview

This Terraform configuration provisions AWS infrastructure for the For Your Service platform, enabling Databricks to read/write data from S3 with proper security and free tier optimization.

### What Gets Deployed

* **S3 Bucket** - Staging storage for job data, resumes, and model weights (< 5 GB for free tier)
* **IAM Role** - Cross-account role allowing Databricks to access S3
* **IAM Policy** - Least privilege S3 access permissions
* **Security** - Encryption, versioning, and public access blocking

### Cost Optimization

✅ **Free Tier Compliant:**
- S3: 5 GB storage (under free tier limit)
- IAM: Always free
- **Total Monthly Cost:** $0.00 with normal usage

---

## Prerequisites

### 1. AWS Account Setup

Follow the IAM security guide: `docs/aws/AWS_IAM_SECURITY_SETUP.md`

- [ ] Root account MFA enabled
- [ ] IAM user created: `foryourservice-app`
- [ ] Custom policy attached: `ForYourServicePolicy`
- [ ] Access keys generated and stored securely

### 2. Required Tools

```bash
# Terraform (>= 1.5.0)
brew install terraform  # macOS
# OR
choco install terraform # Windows

# Verify installation
terraform version

# AWS CLI (optional but recommended)
brew install awscli
aws configure
```

### 3. AWS Credentials

**Option A: AWS CLI Configuration**
```bash
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ********
# Default region: us-east-1
# Default output format: json
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="********"
export AWS_DEFAULT_REGION="us-east-1"
```

**Option C: Databricks Secrets** (See `docs/aws/AWS_IAM_SECURITY_SETUP.md` for setup)

---

## Deployment

### Step 1: Configure Variables

```bash
# Copy example file
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
nano terraform.tfvars
```

**Required Configuration:**

```hcl
# terraform.tfvars
aws_region             = "us-east-1"
environment            = "dev"
databricks_external_id = "your-databricks-external-id"  # ⚠️ REQUIRED
```

**How to Get External ID:**
1. Go to Databricks workspace → Catalog → Storage Credentials
2. Click "Create credential"
3. Choose "Create new IAM role"
4. Copy the External ID shown (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Step 2: Initialize Terraform

```bash
cd terraform/aws
terraform init
```

This downloads the AWS and Random providers.

### Step 3: Plan Deployment

```bash
terraform plan
```

Review the resources that will be created:
- `aws_s3_bucket.fys_databricks_staging`
- `aws_iam_role.databricks_cross_account_role`
- `aws_iam_policy.databricks_s3_access_policy`
- `aws_iam_role_policy_attachment.databricks_s3_attach`

### Step 4: Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted. Deployment takes ~30 seconds.

### Step 5: Save Outputs

```bash
terraform output -json > outputs.json

# View specific outputs
terraform output s3_bucket_name
terraform output databricks_role_arn
```

---

## Databricks Integration

After deployment, configure Databricks to use the S3 bucket:

### 1. Create Storage Credential

```python
# In Databricks notebook
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Get outputs from Terraform
role_arn = "arn:aws:iam::342050998009:role/fys-databricks-cross-account-role"
external_id = "your-databricks-external-id"

# Create storage credential
w.storage_credentials.create(
    name="fys-aws-storage-credential",
    aws_iam_role={
        "role_arn": role_arn,
        "external_id": external_id
    },
    comment="For Your Service S3 staging access"
)
```

### 2. Create External Location

```python
# Get S3 bucket name from Terraform output
s3_bucket = "fys-pipeline-staging-dev-xxxxxxxx"

w.external_locations.create(
    name="fys-s3-staging",
    url=f"s3://{s3_bucket}/",
    credential_name="fys-aws-storage-credential",
    comment="For Your Service staging data location"
)
```

### 3. Test Access

```python
# Write test data
df = spark.createDataFrame([("test", 1)], ["col1", "col2"])
df.write.format("delta").mode("overwrite").save(f"s3://{s3_bucket}/test/")

# Read back
df_read = spark.read.format("delta").load(f"s3://{s3_bucket}/test/")
df_read.show()
```

If successful, you'll see the test data!

---

## Resource Management

### View Current Infrastructure

```bash
terraform show
```

### Update Infrastructure

```bash
# Modify variables or main.tf
nano terraform.tfvars

# Preview changes
terraform plan

# Apply changes
terraform apply
```

### Destroy Infrastructure

⚠️ **WARNING:** This deletes all resources and data!

```bash
terraform destroy
```

Type `yes` when prompted. Use only for cleanup or teardown.

---

## Troubleshooting

### Issue: "Error creating bucket: BucketAlreadyExists"

**Cause:** S3 bucket names are globally unique.

**Fix:** The `random_id` suffix should prevent this, but if it happens:
```bash
terraform destroy
terraform apply  # Gets new random suffix
```

### Issue: "Error assuming IAM role"

**Cause:** Databricks External ID mismatch.

**Fix:**
1. Verify External ID in `terraform.tfvars` matches Databricks
2. Re-deploy: `terraform apply`

### Issue: "Access Denied" from Databricks

**Cause:** IAM policy or trust relationship issue.

**Fix:**
```bash
# Verify role exists
aws iam get-role --role-name fys-databricks-cross-account-role

# Verify policy is attached
aws iam list-attached-role-policies --role-name fys-databricks-cross-account-role
```

### Issue: Databricks can't access S3

**Checklist:**
- [ ] Storage credential created with correct Role ARN
- [ ] External Location created with correct S3 URL
- [ ] External ID matches between Terraform and Databricks
- [ ] S3 bucket name is correct (check `terraform output s3_bucket_name`)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    For Your Service Platform                 │
│                     (7 Eagle Group)                          │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ Databricks Workspace
               │ (Read/Write Data)
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│          AWS Cross-Account IAM Role                          │
│     fys-databricks-cross-account-role                        │
│                                                              │
│  Trust Relationship:                                         │
│  - Principal: arn:aws:iam::414351767826:root                │
│  - Condition: ExternalId = "your-unique-id"                 │
└──────────────┬───────────────────────────────────────────────┘
               │
               │ Assumes Role
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│          IAM Policy: fys-databricks-s3-access-policy         │
│                                                              │
│  Permissions:                                                │
│  - s3:GetObject                                              │
│  - s3:PutObject                                              │
│  - s3:DeleteObject                                           │
│  - s3:ListBucket                                             │
│  - s3:GetBucketLocation                                      │
└──────────────┬───────────────────────────────────────────────┘
               │
               │ Grants Access To
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│          S3 Bucket: fys-pipeline-staging-dev-XXXX            │
│                                                              │
│  Features:                                                   │
│  - Encryption: AES256 (at rest)                              │
│  - Versioning: Enabled                                       │
│  - Public Access: Blocked                                    │
│  - Free Tier: < 5 GB                                         │
│                                                              │
│  Data:                                                       │
│  ├── /jobs/           (Job postings)                         │
│  ├── /resumes/        (Veteran resumes)                      │
│  ├── /models/         (Neural network weights)               │
│  └── /staging/        (Temporary processing)                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Security Best Practices

✅ **Implemented:**
- Least privilege IAM policy (scoped to specific bucket)
- Cross-account access with External ID
- S3 encryption at rest (AES256)
- S3 versioning enabled
- Public access blocked
- Resource tagging for auditability

⚠️ **Recommended:**
- Enable CloudTrail for audit logging
- Set up S3 lifecycle policies for cost optimization
- Configure S3 bucket notifications for monitoring
- Enable MFA Delete for production buckets

---

## References

- [AWS IAM Security Setup](../../docs/aws/AWS_IAM_SECURITY_SETUP.md)
- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Databricks Unity Catalog External Locations](https://docs.databricks.com/unity-catalog/external-locations.html)
- [For Your Service GitHub](https://github.com/For-Your-Service/For-Your-Service)

---

**Last Updated:** 2026-08-13  
**Maintained By:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group
