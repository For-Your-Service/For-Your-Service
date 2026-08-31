"""
01_Intake_Schema_Definition.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# Databricks notebook source
# DBTITLE 1,PII Anonymization Strategy
import hashlib
import uuid

print("="*70)
print("🔒 PII ANONYMIZATION STRATEGY")
print("="*70)

print("\n📍 Cloud Function will anonymize PII before storing to GCS\n")

# Define anonymization rules
anonymization_rules = {
    "personal_info.full_name": "REMOVE - Generate anonymous veteran_id instead",
    "personal_info.email": "HASH - One-way SHA-256 for deduplication only",
    "personal_info.phone": "REMOVE",
    "personal_info.date_of_birth": "GENERALIZE - Keep only birth_year (for age calculation)",
    "personal_info.ssn_last_four": "REMOVE",
    "personal_info.address.street": "REMOVE",
    "personal_info.address.city": "KEEP - Needed for location matching",
    "personal_info.address.state": "KEEP - Needed for location matching",
    "personal_info.address.zip": "GENERALIZE - Keep only first 3 digits (ZIP3)"
}

print("⚙️ Anonymization Rules:\n")
for field, rule in anonymization_rules.items():
    print(f"  • {field:<40} → {rule}")

# Demonstrate anonymization on example
print("\n" + "="*70)
print("🎯 ANONYMIZATION EXAMPLE")
print("="*70)

# Original PII
original_name = "James Rodriguez"
original_email = "j.rodriguez.usmc@example.com"
original_dob = "1990-03-15"
original_zip = "92101"

print(f"\n👤 Original PII:")
print(f"  Name: {original_name}")
print(f"  Email: {original_email}")
print(f"  DOB: {original_dob}")
print(f"  ZIP: {original_zip}")

# Generate anonymous veteran ID (deterministic based on email hash + timestamp)
email_hash = hashlib.sha256(original_email.encode()).hexdigest()[:16]
anonymous_veteran_id = f"VET_{email_hash}"

# Extract birth year only
birth_year = int(original_dob.split('-')[0])
current_year = 2024
age = current_year - birth_year

# ZIP3 (first 3 digits)
zip3 = original_zip[:3]

print(f"\n✅ Anonymized Data:")
print(f"  Veteran ID: {anonymous_veteran_id}")
print(f"  Email Hash: {email_hash}... (for deduplication)")
print(f"  Birth Year: {birth_year} (Age: {age})")
print(f"  ZIP3: {zip3}xx (general area)")
print(f"  Name: [REMOVED]")
print(f"  Full Email: [REMOVED]")
print(f"  Phone: [REMOVED]")

print("\n" + "="*70)
print("🔐 RETENTION POLICY")
print("="*70)

print("""
The anonymized profile will contain:
  ✅ Anonymous veteran_id (unique identifier)
  ✅ Military service data (MOS, rank, branch, deployments)
  ✅ Skills, certifications, education
  ✅ Job preferences (roles, industries, salary range)
  ✅ General location (city, state, ZIP3)
  ✅ Birth year (for age-based matching)
  ✅ Counselor info (for 7 Eagle Group coordination)

  ❌ No direct personal identifiers
  ❌ No contact information
  ❌ No full date of birth
  ❌ No SSN
  ❌ No street address

This allows matching and analytics while protecting veteran privacy.
""")

print("🔒 Anonymization strategy defined!")

# COMMAND ----------

# DBTITLE 1,Example Veteran Profile
import uuid
from datetime import datetime

print("="*70)
print("📄 EXAMPLE VETERAN PROFILE")
print("="*70)

# Create a realistic example veteran profile
example_veteran = {
    "intake_id": str(uuid.uuid4()),
    "timestamp": datetime.now().isoformat(),

    "personal_info": {
        "full_name": "James Rodriguez",
        "email": "j.rodriguez.usmc@example.com",
        "phone": "+1-555-0123",
        "date_of_birth": "1990-03-15",
        "ssn_last_four": "4567",
        "address": {
            "street": "1234 Main Street Apt 5B",
            "city": "San Diego",
            "state": "CA",
            "zip": "92101",
            "country": "USA"
        }
    },

    "military_service": {
        "branch": "Marines",
        "rank": "E-6 (Staff Sergeant)",
        "mos_codes": ["0621", "0627"],  # Field Radio Operator, Ground Mobile Forces Satellite Communications Operator
        "service_start_date": "2008-06-15",
        "service_end_date": "2024-06-14",
        "total_service_years": 16.0,
        "deployments": [
            {
                "location": "Afghanistan (Helmand Province)",
                "start_date": "2010-09-01",
                "end_date": "2011-04-30",
                "role": "Communications NCO"
            },
            {
                "location": "Iraq (Al Anbar)",
                "start_date": "2013-02-15",
                "end_date": "2013-10-30",
                "role": "Radio Chief"
            }
        ],
        "security_clearance": "Secret",
        "clearance_active": True,
        "discharge_type": "Honorable"
    },

    "skills": {
        "technical_skills": [
            "Radio Communications",
            "Satellite Communications",
            "Network Administration",
            "Cybersecurity Basics",
            "Technical Troubleshooting",
            "Equipment Maintenance",
            "Signal Intelligence"
        ],
        "soft_skills": [
            "Leadership",
            "Team Management",
            "Crisis Management",
            "Clear Communication",
            "Problem Solving",
            "Attention to Detail",
            "Work Under Pressure"
        ],
        "languages": [
            {"language": "English", "proficiency": "Native"},
            {"language": "Spanish", "proficiency": "Fluent"},
            {"language": "Pashto", "proficiency": "Basic"}
        ],
        "tools_software": [
            "PRC-117 Radio",
            "AN/PRC-150 HF Radio",
            "Cisco IOS",
            "Microsoft Office Suite",
            "Basic Python Scripting"
        ]
    },

    "education": [
        {
            "degree": "Associate",
            "field_of_study": "Information Technology",
            "institution": "San Diego Community College",
            "graduation_year": 2023,
            "gpa": 3.6
        }
    ],

    "certifications": [
        {
            "name": "CompTIA Security+",
            "issuing_organization": "CompTIA",
            "issue_date": "2023-08-15",
            "expiration_date": "2026-08-15",
            "credential_id": "COMP001234567"
        },
        {
            "name": "CompTIA Network+",
            "issuing_organization": "CompTIA",
            "issue_date": "2022-11-10",
            "expiration_date": "2025-11-10",
            "credential_id": "COMP001234568"
        }
    ],

    "job_preferences": {
        "desired_roles": [
            "Network Administrator",
            "IT Support Specialist",
            "Cybersecurity Analyst",
            "Communications Technician",
            "Field Service Technician"
        ],
        "desired_industries": [
            "Technology",
            "Telecommunications",
            "Defense Contracting",
            "Government (Federal/State)"
        ],
        "preferred_locations": [
            {"city": "San Diego", "state": "CA", "willing_to_relocate": False},
            {"city": "Los Angeles", "state": "CA", "willing_to_relocate": True},
            {"city": "Austin", "state": "TX", "willing_to_relocate": True}
        ],
        "remote_work_preference": "Hybrid",
        "salary_expectation": {
            "min": 65000,
            "max": 85000,
            "currency": "USD"
        },
        "employment_type": ["Full-time", "Contract"],
        "start_date_availability": "2024-08-01"
    },

    "transition_info": {
        "counselor_name": "Sarah Mitchell",
        "counselor_email": "s.mitchell@seveneagles.org",
        "referral_source": "7 Eagle Group Transition Program",
        "urgency_level": "High",
        "veteran_notes": "Excited to transition into IT/cybersecurity. Have been studying for certifications during terminal leave. Strong preference to stay in San Diego area due to family.",
        "counselor_notes": "Highly motivated veteran with strong technical background. Security clearance and recent certifications make him competitive for defense contracting roles. Needs support translating MOS experience to civilian job descriptions."
    },

    "metadata": {
        "intake_version": "1.0.0",
        "intake_platform": "Web",
        "partner_org": "7 Eagle Group"
    }
}

# Display the example
print(f"\n✅ Generated example veteran profile:")
print(f"\nIntake ID: {example_veteran['intake_id']}")
print(f"Name: {example_veteran['personal_info']['full_name']}")
print(f"Branch: {example_veteran['military_service']['branch']}")
print(f"MOS Codes: {', '.join(example_veteran['military_service']['mos_codes'])}")
print(f"Service Years: {example_veteran['military_service']['total_service_years']}")
print(f"Clearance: {example_veteran['military_service']['security_clearance']}")
print(f"\nDesired Roles:")
for role in example_veteran['job_preferences']['desired_roles']:
    print(f"  • {role}")

print(f"\nSalary Range: ${example_veteran['job_preferences']['salary_expectation']['min']:,} - ${example_veteran['job_preferences']['salary_expectation']['max']:,}")

# Save to JSON for reference
import json
json_output = json.dumps(example_veteran, indent=2)

print(f"\n💾 JSON Size: {len(json_output)} bytes")
print(f"\n🔒 This profile contains PII that will be anonymized before storage.")

# COMMAND ----------

# DBTITLE 1,For Your Service - Veteran Profile Schema
# MAGIC %md
# MAGIC # 🎖️ For Your Service - Veteran Profile Schema
# MAGIC
# MAGIC ## Mission Overview
# MAGIC **For Your Service (FYS)** converts qualitative veteran intake data into dynamic, multi-dimensional tensors that compute real-time placement probability matrices against active job postings.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Pipeline Flow
# MAGIC ```
# MAGIC Counselor Intake Wizard
# MAGIC         ↓
# MAGIC     JSON Payload
# MAGIC         ↓
# MAGIC GCP Cloud Function (PII Anonymization)
# MAGIC         ↓
# MAGIC     GCS Raw Bucket
# MAGIC         ↓
# MAGIC Databricks Bronze (Raw Ingestion)
# MAGIC         ↓
# MAGIC Databricks Silver (Feature Engineering)
# MAGIC         ↓
# MAGIC Databricks Gold (Tensor Engine - Vector Dot Products)
# MAGIC         ↓
# MAGIC Placement Probability Matrix
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Integration Partner
# MAGIC **7 Eagle Group** - Veteran placement organization providing counselor network and job posting partnerships.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC This notebook defines the **veteran profile JSON schema** that flows through the entire pipeline.

# COMMAND ----------

# DBTITLE 1,Veteran Profile JSON Schema
import json
from datetime import datetime

print("="*70)
print("🎖️ VETERAN PROFILE INTAKE SCHEMA")
print("="*70)

# Define the complete veteran profile schema
veteran_profile_schema = {
    "intake_id": "uuid",  # Generated by intake system
    "timestamp": "ISO-8601 datetime",

    # ===== PII SECTION (Will be anonymized by Cloud Function) =====
    "personal_info": {
        "full_name": "string (PII)",
        "email": "string (PII)",
        "phone": "string (PII)",
        "date_of_birth": "YYYY-MM-DD (PII)",
        "ssn_last_four": "string (PII - optional for verification)",
        "address": {
            "street": "string (PII)",
            "city": "string",
            "state": "string (2-letter code)",
            "zip": "string",
            "country": "string (default: USA)"
        }
    },

    # ===== MILITARY BACKGROUND =====
    "military_service": {
        "branch": "string (Army, Navy, Air Force, Marines, Coast Guard, Space Force)",
        "rank": "string (E-1 to E-9, O-1 to O-10, W-1 to W-5)",
        "mos_codes": ["list of Military Occupational Specialty codes"],
        "service_start_date": "YYYY-MM-DD",
        "service_end_date": "YYYY-MM-DD",
        "total_service_years": "float",
        "deployments": [{
            "location": "string",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "role": "string"
        }],
        "security_clearance": "string (None, Confidential, Secret, Top Secret, TS/SCI)",
        "clearance_active": "boolean",
        "discharge_type": "string (Honorable, General, etc.)"
    },

    # ===== SKILLS & COMPETENCIES =====
    "skills": {
        "technical_skills": ["list of strings"],
        "soft_skills": ["list of strings (leadership, communication, etc.)"],
        "languages": [{
            "language": "string",
            "proficiency": "string (Basic, Intermediate, Fluent, Native)"
        }],
        "tools_software": ["list of specific tools/software proficiencies"]
    },

    # ===== EDUCATION & CERTIFICATIONS =====
    "education": [{
        "degree": "string (High School, Associate, Bachelor, Master, PhD)",
        "field_of_study": "string",
        "institution": "string",
        "graduation_year": "int",
        "gpa": "float (optional)"
    }],

    "certifications": [{
        "name": "string",
        "issuing_organization": "string",
        "issue_date": "YYYY-MM-DD",
        "expiration_date": "YYYY-MM-DD (optional)",
        "credential_id": "string (optional)"
    }],

    # ===== JOB PREFERENCES =====
    "job_preferences": {
        "desired_roles": ["list of job titles/roles"],
        "desired_industries": ["list of industries"],
        "preferred_locations": [{
            "city": "string",
            "state": "string",
            "willing_to_relocate": "boolean"
        }],
        "remote_work_preference": "string (Required, Preferred, Hybrid, On-site Only)",
        "salary_expectation": {
            "min": "int (annual)",
            "max": "int (annual)",
            "currency": "string (default: USD)"
        },
        "employment_type": ["list (Full-time, Part-time, Contract, etc.)"],
        "start_date_availability": "YYYY-MM-DD"
    },

    # ===== TRANSITION SUPPORT =====
    "transition_info": {
        "counselor_name": "string (7 Eagle Group counselor)",
        "counselor_email": "string",
        "referral_source": "string (how they found FYS)",
        "urgency_level": "string (Low, Medium, High, Critical)",
        "veteran_notes": "string (free-form text)",
        "counselor_notes": "string (free-form text)"
    },

    # ===== METADATA =====
    "metadata": {
        "intake_version": "string (schema version)",
        "intake_platform": "string (Web, Mobile, API)",
        "partner_org": "string (e.g., 7 Eagle Group)"
    }
}

print("\n✅ Schema defined with the following sections:")
for section in veteran_profile_schema.keys():
    print(f"  • {section}")

print("\n🔒 PII Fields (will be anonymized):")
print("  • personal_info.full_name")
print("  • personal_info.email")
print("  • personal_info.phone")
print("  • personal_info.date_of_birth")
print("  • personal_info.ssn_last_four")
print("  • personal_info.address.street")

print("\n✅ Schema documentation complete!")

# COMMAND ----------

