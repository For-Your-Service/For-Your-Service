# Veteran Profile Schema

## Overview
Standardized schema for veteran profiles used in the For Your Service job matching platform.

## Profile Structure

### Personal Information
```json
{
  "veteran_id": "string (UUID)",
  "name": "string",
  "email": "string",
  "phone": "string",
  "location": {
    "city": "string",
    "state": "string",
    "zip": "string",
    "willing_to_relocate": "boolean",
    "remote_preference": "required|preferred|no_preference|no_remote"
  }
}
```

### Military Background
```json
{
  "military_experience": {
    "branch": "Army|Navy|Air Force|Marines|Coast Guard|Space Force",
    "mos_afsc": "string (Military Occupational Specialty)",
    "rank": "string",
    "service_start": "date (YYYY-MM-DD)",
    "service_end": "date (YYYY-MM-DD)",
    "years_of_service": "integer",
    "security_clearance": {
      "level": "None|Secret|Top Secret|TS/SCI",
      "status": "active|expired|inactive",
      "expiration_date": "date (YYYY-MM-DD) or null"
    },
    "deployments": "integer",
    "special_qualifications": ["string"]
  }
}
```

### Professional Experience
```json
{
  "civilian_experience": {
    "total_years": "integer",
    "current_title": "string",
    "current_company": "string",
    "industries": ["string"],
    "seniority_level": "entry|mid|senior|lead|executive"
  }
}
```

### Technical Skills
```json
{
  "skills": {
    "cloud_platforms": ["AWS|Azure|GCP|Oracle Cloud"],
    "programming_languages": ["Python|Java|JavaScript|Go|etc"],
    "devops_tools": ["Terraform|Kubernetes|Docker|Jenkins|etc"],
    "databases": ["SQL|NoSQL|specific database names"],
    "certifications": [
      {
        "name": "string",
        "issuer": "string",
        "date_obtained": "date",
        "expiration_date": "date or null"
      }
    ]
  }
}
```

### Job Preferences
```json
{
  "job_preferences": {
    "target_roles": ["string"],
    "salary_range": {
      "min": "integer",
      "max": "integer",
      "currency": "USD"
    },
    "work_authorization": "US Citizen|Green Card|H1B|etc",
    "employment_type": ["full_time|part_time|contract"],
    "benefits_required": ["healthcare|401k|remote|etc"]
  }
}
```

## Example: William Free Hall Profile

```json
{
  "veteran_id": "wfh-001",
  "name": "William Free Hall",
  "email": "whall4.wh@gmail.com",
  "phone": "(910) 584-3843",
  "location": {
    "city": "Niceville",
    "state": "FL",
    "zip": "32578",
    "willing_to_relocate": true,
    "remote_preference": "preferred"
  },
  "military_experience": {
    "branch": "Army",
    "mos_afsc": "18F (Special Forces Intelligence Sergeant)",
    "rank": "Team Sergeant",
    "service_start": "1999-01-01",
    "service_end": "2017-12-31",
    "years_of_service": 18,
    "security_clearance": {
      "level": "TS/SCI",
      "status": "expired",
      "expiration_date": null
    },
    "deployments": 10,
    "special_qualifications": [
      "Special Forces Qualification Course (SFQC)",
      "18F Intelligence Sergeant",
      "Green Beret"
    ]
  },
  "civilian_experience": {
    "total_years": 10,
    "current_title": "Technical Lead & Solutions Architect",
    "current_company": "For Your Service",
    "industries": ["Technology", "Energy", "Defense"],
    "seniority_level": "executive"
  },
  "skills": {
    "cloud_platforms": ["AWS", "Azure", "GCP"],
    "programming_languages": ["Python", "SQL", "Bash"],
    "devops_tools": [
      "Terraform",
      "Kubernetes",
      "Docker",
      "GitHub Actions",
      "Jenkins"
    ],
    "databases": ["PostgreSQL", "Delta Lake"],
    "certifications": [
      {
        "name": "AWS Certified Cloud Practitioner",
        "issuer": "Amazon Web Services",
        "date_obtained": "2022-01-01",
        "expiration_date": null
      }
    ]
  },
  "job_preferences": {
    "target_roles": [
      "DevOps Engineer",
      "Solutions Architect",
      "Cloud Engineer",
      "Site Reliability Engineer",
      "Platform Engineer"
    ],
    "salary_range": {
      "min": 120000,
      "max": 180000,
      "currency": "USD"
    },
    "work_authorization": "US Citizen",
    "employment_type": ["full_time"],
    "benefits_required": ["healthcare", "401k", "remote"]
  }
}
```

## Validation Rules

1. **Required Fields:** veteran_id, name, email, location, military_experience
2. **Email Format:** Must be valid email format
3. **Phone Format:** US phone number format
4. **Salary Range:** min must be less than max
5. **Dates:** All dates in YYYY-MM-DD format
6. **Service Years:** Calculated from service_start and service_end

## Database Schema (SQL)

```sql
CREATE TABLE veterans (
    veteran_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10),
    willing_to_relocate BOOLEAN DEFAULT FALSE,
    remote_preference VARCHAR(20),

    -- Military
    military_branch VARCHAR(50),
    mos_afsc VARCHAR(100),
    rank VARCHAR(100),
    service_start DATE,
    service_end DATE,
    years_of_service INTEGER,
    clearance_level VARCHAR(20),
    clearance_status VARCHAR(20),
    deployments INTEGER,

    -- Professional
    total_civilian_years INTEGER,
    current_title VARCHAR(255),
    current_company VARCHAR(255),
    seniority_level VARCHAR(20),

    -- Preferences
    salary_min INTEGER,
    salary_max INTEGER,
    work_authorization VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

**Created:** August 10, 2026
**Author:** William Free Hall <whall4.wh@gmail.com>
**Organization:** 7 Eagle Group
