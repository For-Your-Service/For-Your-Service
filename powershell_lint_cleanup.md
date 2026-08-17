# PowerShell Codebase Formatting Workflow
File: powershell_lint_cleanup.md

## 1. Create Root Flake8 Configuration (No BOM)
Set-Content -Path ".flake8" -Value @"
[flake8]
max-line-length = 120
extend-ignore = E501
"@ -Encoding ASCII

## 2. Execute Flake8
flake8 notebooks/
