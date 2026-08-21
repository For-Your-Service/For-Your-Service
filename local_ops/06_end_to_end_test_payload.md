# [BACKLOG] End-to-End Test Payload - Send dummy JSON through Cloud Function into Databricks

## 🏗️ Architecture & Execution Roadmap: PENDING
Executes a full integration test sending a simulated JSON telemetry payload through the live Cloud Function endpoint into GCS storage.

## 🎯 Specific Execution Steps
- [ ] Step 1: Construct test payload object in PowerShell:
  \\\powershell
  $testPayload = @{
      user_id = "test_operator_01"
      event_type = "telemetry_dispatch"
      timestamp = (Get-Date -Format "o")
  } | ConvertTo-Json
  \\\
- [ ] Step 2: Retrieve active Cloud Function URI and dispatch HTTP POST request:
  \\\powershell
  $uri = gcloud functions describe fys-ingest-service --region=us-central1 --format='value(serviceConfig.uri)'
  Invoke-RestMethod -Uri $uri -Method Post -Body $testPayload -ContentType 'application/json'
  \\\

---

# 🗺️ Verification Checklist
- [ ] Confirm HTTP \200 OK\ response status code returned from endpoint
- [ ] Inspect destination GCS bucket for successfully written object:
  \\\powershell
  gcloud storage ls gs://fys-landing-dev/**
  \\\
- [ ] Change task status on the project board to **Done**
