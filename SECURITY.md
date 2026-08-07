# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email:
**whall4.wh@gmail.com**

Do NOT create a public GitHub issue.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Best Practices

### API Keys
* Never commit API keys to Git
* Use environment variables
* Rotate keys regularly
* Use least-privilege access

### Data Handling
* PII is never stored
* All API calls are logged (not payloads)
* Data retention: 90 days max
* Encryption at rest and in transit

### Dependencies
* Regular security updates
* Automated vulnerability scanning
* Pin versions in requirements.txt
