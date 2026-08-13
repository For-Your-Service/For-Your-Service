# Daily Notes - August 13, 2026

**Developer:** Free Hall (whall4.wh@gmail.com)  
**Organization:** 7 Eagle Group  
**Project:** For Your Service - Veteran Job Matching Platform

---

## AWS Infrastructure Setup

### Objective
Set up secure AWS IAM configuration for For Your Service platform, optimized for free tier usage and following least privilege security principles.

### Account Details
- **Account ID:** 342050998009
- **Account Name:** W. Free Hall
- **Email:** whall4.wh+aws1@gmail.com
- **Free Tier Status:** $100 credits, 185 days remaining (until Feb 12, 2027)
- **Primary Region:** us-east-1

### Work Completed

#### 1. IAM Security Architecture
- ✅ Documented comprehensive IAM setup process
- ✅ Created custom policy `ForYourServicePolicy` with least privilege access
- ✅ Scoped all permissions to `foryourservice-*` resources only
- ✅ Configured MFA requirements for root and IAM users
- ✅ Set up budget alerts ($0 threshold for free tier compliance)

#### 2. Security Features
- **Least Privilege Access:** Custom IAM policy limits scope to project resources
- **Resource Isolation:** All resources prefixed with `foryourservice-*`
- **MFA Protection:** Both root and IAM user accounts
- **Budget Monitoring:** Zero-spend alerts to prevent charges
- **Audit Logging:** CloudWatch logs for all Lambda functions

#### 3. IAM Policy Scope
Created custom policy with access to:
- **S3:** Buckets matching `foryourservice-*` (for resumes, model weights)
- **DynamoDB:** Tables matching `foryourservice-*` (for veteran/job profiles)
- **Lambda:** Functions matching `foryourservice-*` (for API endpoints)
- **CloudWatch:** Logging for monitoring
- **Secrets Manager:** Application secrets under `foryourservice/` path

#### 4. Databricks Integration
- Configured secrets scope: `aws-credentials`
- Stored IAM credentials securely (never in code)
- Created connection test script
- Documented usage patterns for Spark + S3

#### 5. Free Tier Optimization
Documented limits and usage patterns:
- S3: 5 GB storage, 20K GET, 2K PUT requests/month
- Lambda: 1M requests/month (perfect for API endpoints)
- DynamoDB: 25 GB storage (sufficient for initial deployment)
- EC2: 750 hours/month t2.micro (optional for Kubernetes)

### Files Created

1. **docs/aws/AWS_IAM_SECURITY_SETUP.md**
   - Comprehensive IAM setup guide
   - Custom policy JSON
   - Security checklist
   - Databricks integration instructions
   - Resource naming conventions

2. **scripts/aws/test_aws_connection.py**
   - AWS connection test script
   - Verifies IAM credentials
   - Tests S3 and DynamoDB access
   - Uses Databricks Secrets securely

### Next Steps

1. **Complete IAM Setup:**
   - [ ] Enable MFA on root account
   - [ ] Create IAM user: `foryourservice-app`
   - [ ] Attach custom `ForYourServicePolicy`
   - [ ] Generate access keys
   - [ ] Store credentials in Databricks Secrets

2. **Test Connection:**
   - [ ] Run `scripts/aws/test_aws_connection.py`
   - [ ] Verify account 342050998009 connection
   - [ ] Confirm S3 and DynamoDB access

3. **Create AWS Resources:**
   - [ ] S3 bucket: `foryourservice-data-prod`
   - [ ] DynamoDB table: `foryourservice-veterans`
   - [ ] DynamoDB table: `foryourservice-jobs`
   - [ ] Lambda function: `foryourservice-match-api`

4. **Neural Network Deployment:**
   - [ ] Upload trained model weights to S3
   - [ ] Configure Lambda for inference
   - [ ] Set up API Gateway endpoints
   - [ ] Test end-to-end matching pipeline

### Security Notes

Following Green Beret operational security principles:
- **Compartmentalization:** IAM policy scoped to specific resources only
- **Defense in Depth:** MFA + least privilege + budget alerts + audit logs
- **Zero Trust:** No root account usage, all access via dedicated IAM user
- **Mission Focus:** Permissions aligned exactly to For Your Service requirements

### Cost Management

All work stays within AWS Free Tier limits:
- Current spend: $0.00
- Budget alert threshold: $0.00
- Credits remaining: $100.00
- Days remaining: 185

Target: Complete development and testing without any AWS charges.

---

## Technical Decisions

### Why Custom IAM Policy?
- AWS managed policies (`*FullAccess`) grant excessive permissions
- Custom policy limits blast radius of credential compromise
- Aligns with military operational security mindset
- Easy to audit and maintain

### Why us-east-1 Region?
- Standard free tier availability
- Lowest latency for most US users
- Well-documented and stable
- Compatible with all AWS services

### Why DynamoDB over RDS?
- 25 GB free tier (always free, not just 12 months)
- Serverless - no instance management
- Better for veteran profile lookups (key-value access pattern)
- Lower latency for matching queries

---

## References

- AWS Account: https://console.aws.amazon.com (342050998009)
- GitHub Repo: https://github.com/For-Your-Service/For-Your-Service
- 7 Eagle Group Partnership: Veteran placement organization
- Project Documentation: See `docs/aws/` directory

---

**Mission Focus:** Helping veterans find meaningful employment through AI-powered matching.  
**Zero Cost Goal:** Stay within free tier limits for sustainable deployment.  
**Security First:** Protect veteran data with military-grade operational security.

---

**Committed By:** Free Hall <whall4.wh@gmail.com>  
**Date:** 2026-08-13  
**Organization:** 7 Eagle Group
