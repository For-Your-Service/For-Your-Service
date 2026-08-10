# Security Best Practices

## API Key Management

### ✅ DO
- Store ALL keys in Databricks Secrets
- Use separate secrets scope per environment
- Rotate keys every 90 days
- Monitor API key usage
- Use service accounts for production

### ❌ DON'T
- Commit keys to Git
- Share keys via email/Slack
- Use personal keys in production
- Store keys in notebook variables
- Log API keys

## Data Security

### PII Handling
- Veteran SSN → Hash before storage
- Contact info → Encrypted at rest
- Resume text → Stored in secure volume
- Audit all PII access

### Access Control
- Use Unity Catalog GRANTS
- Row-level security for multi-tenant
- Column masking for sensitive fields
- Audit logs enabled

## Network Security
- API calls over HTTPS only
- Verify SSL certificates
- Use IP allowlists where possible
- Enable VPC peering for production

## Incident Response
1. Detect: Monitor for unusual API usage
2. Contain: Rotate compromised keys immediately
3. Investigate: Check audit logs
4. Remediate: Fix vulnerability
5. Document: Update runbook
