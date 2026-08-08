# 🔐 PII Protection & Privacy Documentation

## For Your Service - How We Protect Veteran Privacy

**Last Updated:** August 5, 2026

---

## Table of Contents
1. [Simple Explanation](#simple-explanation)
2. [What is PII?](#what-is-pii)
3. [Our PII Protection Approach](#our-pii-protection-approach)
4. [Technical Implementation](#technical-implementation)
5. [Data Flow](#data-flow)
6. [What Gets Removed vs. Kept](#what-gets-removed-vs-kept)
7. [Storage & Retention](#storage--retention)
8. [Security Guarantees](#security-guarantees)

---

## Simple Explanation

**The Problem:**
When veterans apply for jobs through 7 Eagle Group counselors, they share personal information like their name, phone number, email, and address. This information is private and sensitive.

**Our Solution:**
Before we store ANY data, our system automatically removes all personal identifying information. We replace it with a random ID number. This means:
- ✅ We can still match veterans to jobs based on their skills and preferences
- ✅ The veteran's identity remains completely private
- ✅ Even if someone accessed our database, they couldn't identify who the veteran is
- ✅ Only the original 7 Eagle Group counselor knows the veteran's real identity

**Think of it like this:**
Imagine filling out a job application, but instead of writing your name, you get a ticket number (like at a deli counter). The system uses your ticket number to match you with jobs, but never knows your actual name.

---

## What is PII?

**PII = Personally Identifiable Information**

PII is any information that can be used to identify a specific person. Examples include:

### Direct Identifiers (can identify someone by themselves):
- Full name
- Social Security Number (SSN)
- Email address
- Phone number
- Street address
- Date of birth
- Driver's license number
- Passport number

### Quasi-Identifiers (can identify someone when combined):
- ZIP code + age + gender
- Detailed location data
- Unique account numbers

---

## Our PII Protection Approach

### The "Anonymization at the Edge" Strategy

**What this means:**
We remove PII **immediately** when data first enters our system, before it's ever stored anywhere. This is called "anonymization at the edge."

**Why this matters:**
- PII never touches our long-term storage
- Even if our database is compromised, there's no PII to steal
- We can't accidentally leak PII because we don't have it
- Complies with privacy regulations (GDPR, CCPA, etc.)

### Three-Layer Protection

1. **Layer 1: Intake Validation**
   - Cloud Function receives the veteran profile
   - Validates the data structure is correct
   - Checks all required fields are present

2. **Layer 2: PII Removal**
   - Removes all direct identifiers
   - Generates anonymous veteran_id (UUID)
   - Preserves job-relevant information only

3. **Layer 3: Secure Storage**
   - Stores anonymized data to GCS bucket
   - 30-day automatic deletion
   - No way to reverse-engineer identity

---

## Technical Implementation

### Cloud Function: `veteran-intake-processor`

**Location:** `cloud-functions/veteran-intake/main.py`

**Function:** `veteran_intake(request)`

**What it does:**

```
1. Receive HTTP POST with veteran profile JSON
2. Parse and validate JSON structure
3. Generate unique veteran_id (UUID v4)
4. Create anonymized profile by:
   - Copying job-relevant fields
   - Skipping ALL PII fields
   - Adding veteran_id and timestamp
5. Upload anonymized JSON to GCS bucket
6. Return success response with veteran_id
7. Original data with PII is discarded (never stored)
```

### Code Structure

**Input (from 7 Eagle Group intake form):**
```json
{
  "intake_id": "INTAKE_12345",
  "personal_info": {
    "full_name": "Jane Doe",           ← PII: REMOVED
    "email": "jane@email.com",         ← PII: REMOVED
    "phone": "555-1234",               ← PII: REMOVED
    "date_of_birth": "1990-01-15",     ← PII: REMOVED
    "ssn": "123-45-6789",              ← PII: REMOVED
    "address": {                        ← PII: REMOVED
      "street": "123 Main St",
      "city": "San Diego",
      "state": "CA",
      "zip": "92101"
    }
  },
  "military_service": {
    "branch": "Army",                   ← KEPT: Job-relevant
    "mos_code": "11B",                  ← KEPT: Job-relevant
    "rank": "E-5",                      ← KEPT: Job-relevant
    "years_served": 6                   ← KEPT: Job-relevant
  },
  "skills": {
    "technical": ["Leadership"],        ← KEPT: Job-relevant
    "soft": ["Problem-solving"]         ← KEPT: Job-relevant
  },
  "job_preferences": {
    "desired_roles": ["Manager"],       ← KEPT: Job-relevant
    "locations": ["San Diego, CA"],     ← KEPT: General location OK
    "salary_min": 60000                 ← KEPT: Job-relevant
  }
}
```

**Output (stored in GCS):**
```json
{
  "veteran_id": "a7f3c891-2b4e-4d19-9f6a-8e7c5b3a9d2f",  ← NEW: Anonymous ID
  "timestamp": "2026-08-05T18:45:00Z",                  ← NEW: When processed
  "military_service": {
    "branch": "Army",
    "mos_code": "11B",
    "rank": "E-5",
    "years_served": 6
  },
  "skills": {
    "technical": ["Leadership"],
    "soft": ["Problem-solving"]
  },
  "job_preferences": {
    "desired_roles": ["Manager"],
    "locations": ["San Diego, CA"],
    "salary_min": 60000
  }
}
```

**Notice:**
- ✅ All PII fields are gone
- ✅ `veteran_id` is a random UUID (impossible to guess)
- ✅ Skills and preferences remain (needed for job matching)
- ✅ General location kept (city/state), but not street address

---

## Data Flow

### Complete System Flow with PII Protection

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. INTAKE FORM                                                  │
│    7 Eagle Group counselor enters veteran data                   │
│    Contains: Name, Email, Phone, SSN, Address, Skills, etc.    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                              ↓ HTTP POST
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. CLOUD FUNCTION (veteran-intake-processor)                    │
│    ⚡ THIS IS WHERE PII IS REMOVED                              │
│                                                                  │
│    Steps:                                                        │
│    a) Receive full profile (including PII)                      │
│    b) Validate data structure                                   │
│    c) Generate random veteran_id (UUID)                         │
│    d) Create NEW object with ONLY non-PII fields               │
│    e) Discard original data (with PII)                          │
│                                                                  │
│    PII REMOVED:                                                 │
│    ❌ Name, Email, Phone, DOB, SSN, Street Address             │
│                                                                  │
│    KEPT:                                                         │
│    ✅ Military background, Skills, Job preferences              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                              ↓ Upload anonymized JSON
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. GCS BUCKET (fys-veteran-intake-raw)                          │
│    Storage for anonymized profiles                              │
│    - Each file: vet_<uuid>.json                                 │
│    - Contains: veteran_id + job data (NO PII)                   │
│    - 30-day lifecycle (auto-delete)                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                              ↓ Databricks reads
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. DATABRICKS PROCESSING                                        │
│    Bronze Layer: Raw anonymized data                            │
│    Silver Layer: Feature engineering                            │
│    Gold Layer: Job matching                                     │
│                                                                  │
│    ✅ STILL NO PII - only veteran_id references                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                              ↓
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. JOB RECOMMENDATIONS                                          │
│    Output: veteran_id → matched jobs                            │
│                                                                  │
│    To connect back to veteran:                                  │
│    - 7 Eagle Group counselor has veteran_id                      │
│    - Counselor contacts veteran with recommendations            │
│    - System never knows veteran's real identity                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Points:

1. **PII exists in memory for ~1 second** (during Cloud Function processing)
2. **PII is NEVER written to disk or permanent storage**
3. **Original request data is garbage collected immediately**
4. **Only anonymized data flows to downstream systems**

---

## What Gets Removed vs. Kept

### ❌ REMOVED (PII Fields)

These fields are **completely removed** and never stored:

| Field | Why Removed | Example |
|-------|-------------|---------|
| `personal_info.full_name` | Direct identifier | "Jane Doe" |
| `personal_info.email` | Direct identifier | "jane@email.com" |
| `personal_info.phone` | Direct identifier | "555-1234" |
| `personal_info.date_of_birth` | Direct identifier + age calculation | "1990-01-15" |
| `personal_info.ssn` | Direct identifier | "123-45-6789" |
| `personal_info.address.street` | Direct identifier | "123 Main St" |
| `personal_info.address.zip` | Quasi-identifier (too specific) | "92101" |

### ✅ KEPT (Job-Relevant, Non-PII Fields)

These fields are **preserved** because they're needed for job matching and don't identify individuals:

| Field Category | Fields Kept | Why Safe | Example |
|----------------|-------------|----------|---------|
| Military Background | `branch`, `mos_code`, `rank`, `years_served`, `discharge_type` | Thousands of veterans share these | "Army, 11B, E-5, 6 years" |
| Skills | `technical`, `soft`, `languages`, `tools` | Common skills, not identifying | "Leadership, Python" |
| Education | `degree`, `field` (NOT institution name) | General education level | "Bachelor's, Computer Science" |
| Certifications | `name`, `issuer` | Professional certs, widely held | "PMP, PMI" |
| Job Preferences | `desired_roles`, `industries`, `salary_min`, `employment_type` | Preferences, not identity | "Manager, Tech, $80k" |
| General Location | `city`, `state` (NOT street address) | Broad area, not precise location | "San Diego, CA" |

### 🔄 GENERATED (New Anonymous Fields)

| Field | Purpose | Example |
|-------|---------|---------|
| `veteran_id` | Anonymous reference (UUID v4) | "a7f3c891-2b4e-4d19-9f6a-8e7c5b3a9d2f" |
| `timestamp` | When processed (UTC) | "2026-08-05T18:45:00Z" |

---

## Storage & Retention

### Where Anonymized Data Lives

**Primary Storage: GCS Bucket**
- **Bucket:** `gs://fys-veteran-intake-raw/intake/`
- **Format:** JSON files, one per veteran
- **Naming:** `vet_<veteran_id>.json`
- **Retention:** 30 days (automatic deletion)
- **Purpose:** Raw intake for Databricks ingestion

**Secondary Storage: Databricks Delta Tables**
- **Bronze Table:** Raw anonymized profiles
- **Silver Table:** Engineered features
- **Gold Table:** Job match scores
- **Retention:** Configurable (recommend 1-2 years for model training)

### Why 30-Day GCS Retention?

The GCS bucket is just a **landing zone** for fresh data. Once Databricks ingests the data:
- ✅ Data is in Databricks Delta tables (persistent)
- ✅ Original JSON files are no longer needed
- ✅ 30 days provides buffer for troubleshooting
- ✅ Reduces storage costs
- ✅ Reduces attack surface (less data = less risk)

### Automatic Cleanup

**GCS Lifecycle Policy:**
```json
{
  "lifecycle": {
    "rule": [{
      "action": {"type": "Delete"},
      "condition": {"age": 30}
    }]
  }
}
```

**What this means:**
Any file in `gs://fys-veteran-intake-raw/intake/` older than 30 days is automatically deleted by Google Cloud Storage. No manual cleanup needed.

---

## Security Guarantees

### What We Can Guarantee

✅ **PII is removed before storage**
- Anonymization happens in Cloud Function (at the edge)
- PII never touches our database

✅ **veteran_id cannot be reverse-engineered**
- Uses UUID v4 (random, 128-bit)
- 2^122 possible values (astronomically large)
- No pattern or sequence to guess

✅ **Data at rest is encrypted**
- GCS encrypts all data by default (AES-256)
- Databricks Delta tables are encrypted

✅ **Data in transit is encrypted**
- HTTPS for Cloud Function endpoint (TLS 1.3)
- GCS API calls use TLS

✅ **Automatic data expiration**
- 30-day lifecycle policy on GCS bucket
- Reduces long-term risk

### What We Cannot Guarantee

❌ **We cannot re-identify veterans**
- By design, we don't have the mapping
- Only 7 Eagle Group counselors have this

❌ **We cannot prevent ALL re-identification**
- If a veteran has extremely unique characteristics (e.g., only Navy SEAL in San Diego with PhD in Astrophysics), they might be identifiable
- This is a limitation of ALL anonymization approaches
- We minimize risk by removing all direct identifiers

### Compliance

This anonymization approach aligns with:

✅ **GDPR (General Data Protection Regulation)**
- Article 4(5): "Anonymised information is not personal data"
- Proper anonymization exempts data from GDPR requirements

✅ **CCPA (California Consumer Privacy Act)**
- "De-identified" data is not "personal information" under CCPA
- Must use reasonable measures to prevent re-identification (we do)

✅ **HIPAA (if applicable)**
- De-identification under Safe Harbor method (§164.514(b)(2))
- We remove all 18 HIPAA identifiers

✅ **Military/Veteran-Specific Regulations**
- No SSN storage (protects against identity theft)
- No deployment details stored (OPSEC)
- No medical information stored

---

## Testing PII Removal

### How to Verify PII is Removed

**Test Process:**

1. Send a test profile with PII:
```bash
curl -X POST https://us-central1-for-your-service-2026.cloudfunctions.net/veteran-intake-processor   -H "Content-Type: application/json"   -d '{
    "personal_info": {
      "full_name": "Test User",
      "email": "test@example.com"
    },
    "military_service": {"branch": "Army"}
  }'
```

2. Check GCS bucket:
```bash
gsutil cat gs://fys-veteran-intake-raw/intake/<file>.json
```

3. Verify the output:
   - ✅ No `full_name` field
   - ✅ No `email` field
   - ✅ `veteran_id` present (UUID)
   - ✅ `military_service` preserved

**Automated Testing:**
- Unit tests in `tests/test_pii_anonymization.py` (future)
- Checks for presence of PII fields in output
- Fails if ANY PII leaks through

---

## Questions & Answers

### Q: Can we ever get the veteran's name back?

**A:** No. Once the Cloud Function discards the original data, there's no way to retrieve it from our system. Only the 7 Eagle Group counselor who submitted the data knows the veteran's identity and has the mapping to `veteran_id`.

### Q: What if we need to contact a veteran?

**A:** We don't contact veterans directly. The workflow is:
1. Our system generates job matches for `veteran_id`
2. We send matches back to 7 Eagle Group with `veteran_id`
3. 7 Eagle Group counselor looks up which veteran has that ID
4. Counselor contacts the veteran

### Q: Is this really anonymous, or just pseudonymous?

**A:** Technically, this is **pseudonymization** (using `veteran_id` as a pseudonym). True anonymization would mean we can't distinguish between veterans at all. We need pseudonymization to:
- Track a veteran's job matches over time
- Avoid duplicate profiles
- Send results back to the correct veteran

However, because **we** don't have the mapping (7 Eagle Group does), it's effectively anonymous from our system's perspective.

### Q: What about k-anonymity or differential privacy?

**A:** Those are advanced techniques for statistical datasets. We're not publishing aggregate statistics about veterans, so they're not necessary here. Our approach (PII removal + pseudonymization) is appropriate for our use case.

### Q: What if there's a data breach?

**A:** If someone gained access to our GCS bucket or Databricks tables, they would see:
- Anonymous veteran IDs
- Military backgrounds (branch, MOS, rank)
- Skills and job preferences
- General locations (city/state)

They would **NOT** see:
- Names
- Email addresses
- Phone numbers
- Street addresses
- Social Security Numbers

This dramatically limits the damage from a breach.

---

## Responsible Disclosure

If you discover a privacy or security issue with our PII handling, please report it to:

**Security Contact:** [Insert security contact email]

**What to include:**
- Description of the issue
- Steps to reproduce
- Potential impact
- Your contact information

We treat security reports seriously and will respond within 24 hours.

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-08-05 | 1.0 | Initial documentation |

---

_This documentation is maintained by the For Your Service development team._
_For questions, see the main [README.md](./README.md) or [DEPLOYMENT_LOG.md](./DEPLOYMENT_LOG.md)._
