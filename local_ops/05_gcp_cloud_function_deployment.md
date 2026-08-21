# [IN PROGRESS] GCP Cloud Function Deployment - Deploy src/ingestion to GCP and create gcs bucket

## 🏗️ Architecture & Execution Roadmap: IN PROGRESS
Provisions the live serverless infrastructure on Google Cloud Platform, creating the GCS storage bucket and deploying the ingestion service code.

## 🎯 Specific Execution Steps
- [ ] Step 1: Authenticate and select target GCP project context via \gcloud auth list\
- [ ] Step 2: Create the GCS landing bucket in \us-central1\:
  \\\powershell
  gcloud storage buckets create gs://fys-landing-dev --location=us-central1
  \\\
- [ ] Step 3: Deploy the ingestion service as a Gen 2 Cloud Function:
  \\\powershell
  gcloud functions deploy fys-ingest-service --gen2 --runtime=python311 --region=us-central1 --source=./src/ingestion --entry-point=ingest_payload --trigger-http --allow-unauthenticated
  \\\

---

# 🗺️ Verification Checklist
- [ ] Verify bucket creation via \gcloud storage buckets list --filter='name:fys-landing-dev'\
- [ ] Extract active HTTP service URL using \gcloud functions describe fys-ingest-service --region=us-central1 --format='value(serviceConfig.uri)'\
- [ ] Change task status on the project board to **Done**
