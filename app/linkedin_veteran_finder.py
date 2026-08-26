#!/usr/bin/env python3
"""
File: app/linkedin_veteran_finder.py
Description: Dynamic Veteran Talent Intelligence & LinkedIn Recon Engine
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Gunslinger Clean-Core (Veteran-First Priority)
"""

import urllib.parse
import json
import re
from typing import List, Dict, Any, Optional
import pandas as pd

DEFAULT_COMPANIES = [
    "GE Aerospace",
    "General Electric",
    "Lockheed Martin",
    "Boeing",
    "Pratt & Whitney",
    "Raytheon Technologies",
    "Northrop Grumman",
    "L3Harris",
    "General Dynamics",
    "Amazon Web Services",
    "Microsoft Defense",
    "Palantir Technologies",
    "Booz Allen Hamilton"
]

DEFAULT_ROLES = [
    "Sr AI Data Engineer",
    "Senior AI Data Engineer",
    "Staff Data Engineer",
    "AI Data Architect",
    "Machine Learning Engineer",
    "Databricks Lakehouse Architect",
    "Cloud Infrastructure Engineer",
    "Principal Data Engineer",
    "Engineering Manager",
    "Technical Leader"
]

DEFAULT_LOCATIONS = [
    "Greenville, SC",
    "Greenville-Spartanburg-Anderson, SC",
    "South Carolina",
    "Remote",
    "Huntsville, AL",
    "Atlanta, GA",
    "Washington DC",
    "Dallas-Fort Worth, TX",
    "Seattle, WA",
    "Tampa, FL"
]

MILITARY_KEYWORDS = [
    "Veteran",
    "US Army",
    "Special Forces",
    "Green Beret",
    "US Navy",
    "US Air Force",
    "US Marine Corps",
    "Space Force",
    "DoD",
    "Security Clearance",
    "TS/SCI",
    "Secret Clearance",
    "MOS",
    "AFSC",
    "NCO",
    "Officer"
]

TALENT_LEDGER_DATA = [
    {
        "name": "William Free Hall",
        "company": "GE Aerospace",
        "title": "Senior AI Data Engineer & Lakehouse Architect",
        "location": "Greenville, SC",
        "branch": "US Army (Special Forces / 18F / 18Z)",
        "clearance": "TS/SCI",
        "is_veteran": True,
        "skills": "PySpark, Databricks Unity Catalog, Delta Lake, Istio, PyTorch",
        "profile_url": "https://github.com/FreeFades2Black"
    },
    {
        "name": "Marcus Vance",
        "company": "GE Aerospace",
        "title": "Lead Telemetry & Edge AI Engineer",
        "location": "Greenville, SC",
        "branch": "US Air Force (AFSC 17D Cyberspace Ops)",
        "clearance": "Secret",
        "is_veteran": True,
        "skills": "Turbine Telemetry, Python, AWS IoT, Kafka, Spark Streaming",
        "profile_url": "https://linkedin.com"
    },
    {
        "name": "Elena Rostova",
        "company": "Lockheed Martin",
        "title": "Staff AI Data Architect",
        "location": "Greenville, SC",
        "branch": "US Navy (Information Warfare)",
        "clearance": "TS/SCI",
        "is_veteran": True,
        "skills": "Cloud Infrastructure, Kubernetes, PySpark, Feature Store",
        "profile_url": "https://linkedin.com"
    },
    {
        "name": "James Henderson",
        "company": "Pratt & Whitney",
        "title": "Senior Machine Learning Engineer",
        "location": "Remote",
        "branch": "US Marine Corps (0671 Data Specialist)",
        "clearance": "Secret",
        "is_veteran": True,
        "skills": "Predictive Maintenance, PyTorch, Scikit-Learn, Docker",
        "profile_url": "https://linkedin.com"
    },
    {
        "name": "David Sterling",
        "company": "Boeing",
        "title": "Principal Data Engineer",
        "location": "Seattle, WA",
        "branch": "US Army (25B Information Technology)",
        "clearance": "Secret",
        "is_veteran": True,
        "skills": "Delta Lake, Databricks, SQL, Terraform, CI/CD",
        "profile_url": "https://linkedin.com"
    },
    {
        "name": "Sarah Connor",
        "company": "Raytheon Technologies",
        "title": "Senior Systems Engineer",
        "location": "Huntsville, AL",
        "branch": "Civilian",
        "clearance": "Secret",
        "is_veteran": False,
        "skills": "Radar Telemetry, C++, Linux Daemons, Systems Modeling",
        "profile_url": "https://linkedin.com"
    },
    {
        "name": "Devon Miller",
        "company": "Northrop Grumman",
        "title": "DevSecOps & Platform Engineer",
        "location": "Washington DC",
        "branch": "US Space Force (Cyber Operations)",
        "clearance": "TS/SCI",
        "is_veteran": True,
        "skills": "Helm 3, Istio Service Mesh, Kubernetes, Terraform, AWS GovCloud",
        "profile_url": "https://linkedin.com"
    },
    {
        "name": "Rachel Zane",
        "company": "Amazon Web Services",
        "title": "Senior Solutions Architect (Defense & AI)",
        "location": "Remote",
        "branch": "US Navy (Cryptologic Technician)",
        "clearance": "TS/SCI",
        "is_veteran": True,
        "skills": "AWS SageMaker, EKS, Zero-Trust Architecture, Lakehouse",
        "profile_url": "https://linkedin.com"
    }
]


class LinkedInVeteranFinder:
    """
    Dynamic Veteran Talent Reconnaissance Engine.
    Prioritizes Veteran Insiders at target organizations as the initial tactical foot-in-the-door.
    """

    def __init__(
        self,
        company: str = "GE Aerospace",
        role: str = "Sr AI Data Engineer",
        location: str = "Greenville, SC",
        branch_filter: Optional[str] = None,
        veteran_priority: bool = True
    ):
        self.company = company.strip() if company else "GE Aerospace"
        self.role = role.strip() if role else "Sr AI Data Engineer"
        self.location = location.strip() if location else "Greenville, SC"
        self.branch_filter = branch_filter
        self.veteran_priority = veteran_priority

    def generate_boolean_query(self) -> str:
        """
        Dynamically constructs an advanced Google/Bing X-Ray Boolean query.
        For GE Aerospace Greenville, prioritizes veteran engineers & technical leaders.
        """
        # Dynamic Company clause
        if not self.company or self.company.lower() in ["any", "all", "*"]:
            company_clause = ""
        elif "ge" in self.company.lower() or "general electric" in self.company.lower():
            company_clause = '("GE Aerospace" OR "General Electric" OR "GE Aviation")'
        else:
            comps = [c.strip() for c in self.company.split(",") if c.strip()]
            if len(comps) > 1:
                company_clause = "(" + " OR ".join([f'"{c}"' for c in comps]) + ")"
            else:
                company_clause = f'"{self.company}"'

        # Dynamic Location clause
        if not self.location or self.location.lower() in ["any", "all", "*"]:
            loc_clause = ""
        elif "greenville" in self.location.lower():
            loc_clause = '("Greenville" OR "Spartanburg" OR "South Carolina" OR "SC")'
        elif "remote" in self.location.lower():
            loc_clause = '("Remote" OR "United States")'
        elif ";" in self.location:
            locs = [l.strip() for l in self.location.split(";") if l.strip()]
            loc_clause = "(" + " OR ".join([f'"{l}"' for l in locs]) + ")"
        else:
            loc_clause = f'"{self.location}"'

        # Military background clause
        if self.branch_filter and self.branch_filter not in ["All", "All Veterans"]:
            military_clause = f'("{self.branch_filter}" OR "Veteran" OR "Military")'
        else:
            military_clause = '("Veteran" OR "Army" OR "Navy" OR "Air Force" OR "Marine" OR "Special Forces" OR "DoD" OR "Clearance")'

        # Dynamic Role / Department clause
        if "ge" in self.company.lower() and "greenville" in self.location.lower() and self.veteran_priority:
            role_clause = '("Engineer" OR "Data" OR "Manager" OR "Leader" OR "Architect" OR "Software" OR "AI")'
        elif not self.role or self.role.lower() in ["any", "all", "*"]:
            role_clause = '("Data Engineer" OR "AI Engineer" OR "Software Engineer" OR "Architect")'
        else:
            roles = [r.strip() for r in self.role.split(",") if r.strip()]
            if len(roles) > 1:
                role_clause = "(" + " OR ".join([f'"{r}"' for r in roles]) + ")"
            else:
                clean_role = self.role.replace("Sr.", "Senior").replace("Sr", "Senior")
                role_clause = f'("{self.role}" OR "{clean_role}" OR "Data Engineer" OR "Engineer")'

        # Assemble clauses
        clauses = ["site:linkedin.com/in"]
        if company_clause:
            clauses.append(company_clause)
        if loc_clause:
            clauses.append(loc_clause)
        clauses.append(military_clause)
        if role_clause:
            clauses.append(role_clause)

        return " ".join(clauses)

    def generate_google_search_url(self) -> str:
        """Generates Google X-Ray Search URL."""
        query = self.generate_boolean_query()
        encoded = urllib.parse.quote_plus(query)
        return f"https://www.google.com/search?q={encoded}"

    def generate_duckduckgo_url(self) -> str:
        """Generates DuckDuckGo X-Ray Search URL."""
        query = self.generate_boolean_query()
        encoded = urllib.parse.quote_plus(query)
        return f"https://duckduckgo.com/?q={encoded}"

    def generate_direct_linkedin_search_url(self) -> str:
        """Generates direct LinkedIn People Search URL with pre-filled filters."""
        keywords = f"{self.company} {self.location} Veteran {self.role}".strip()
        encoded = urllib.parse.quote_plus(keywords)
        return f"https://www.linkedin.com/search/results/people/?keywords={encoded}&origin=GLOBAL_SEARCH_HEADER"

    def search_talent_ledger(self, veteran_only: bool = True) -> pd.DataFrame:
        """
        Dynamically filters the talent ledger dataframe.
        Enforces veteran_only priority by default.
        """
        df = pd.DataFrame(TALENT_LEDGER_DATA)
        mask = pd.Series([True] * len(df))
        
        if self.company and self.company.lower() not in ["any", "all", "*"]:
            clean_c = self.company.lower()
            if "ge" in clean_c or "general electric" in clean_c:
                mask &= df['company'].str.contains("GE|General Electric", case=False, na=False)
            else:
                mask &= df['company'].str.contains(re.escape(self.company), case=False, na=False)
                
        if self.role and self.role.lower() not in ["any", "all", "*"] and not self.veteran_priority:
            role_keywords = self.role.replace("Sr", "").replace("Senior", "").strip().split()
            if role_keywords:
                role_pattern = "|".join([re.escape(kw) for kw in role_keywords if len(kw) > 2])
                if role_pattern:
                    mask &= df['title'].str.contains(role_pattern, case=False, na=False)
                    
        if self.location and self.location.lower() not in ["any", "all", "*"]:
            clean_loc = self.location.split(",")[0].strip()
            mask &= df['location'].str.contains(re.escape(clean_loc), case=False, na=False)
            
        if veteran_only:
            mask &= (df['is_veteran'] == True)
            
        if self.branch_filter and self.branch_filter not in ["All", "All Veterans"]:
            mask &= df['branch'].str.contains(re.escape(self.branch_filter), case=False, na=False)
            
        results = df[mask].copy()
        return results

    def generate_shared_patch_connection_note(
        self,
        peer_name: str = "[Name]",
        company_name: Optional[str] = None,
        location_name: Optional[str] = None
    ) -> str:
        """
        High-impact, concise LinkedIn connection request template (under 300 characters).
        Leverages military service bond to break the ice directly with GE Aerospace veterans.
        """
        comp = company_name or self.company
        loc = location_name or self.location
        loc_short = loc.split(",")[0].strip() if "," in loc else loc
        
        return f"Hi {peer_name}, saw you're making waves over at {comp} in {loc_short}. As a retired Special Forces Green Beret / Tech Lead transitioning into senior data engineering in the local area, I'm looking to connect with fellow veterans in the tech stack there. Would love to swap notes for 10 minutes if you're open to it."

    def generate_peer_outreach_message(
        self,
        peer_name: str = "[First Name]",
        sender_name: str = "Free Hall",
        sender_branch: str = "US Army Special Forces (18F / 18Z, Ret.)",
        target_role: Optional[str] = None
    ) -> str:
        """Generates full warm veteran-to-veteran peer message."""
        role_label = target_role or self.role
        message = f"""Hi {peer_name},

I saw your profile and noticed your transition from military service to engineering at {self.company}. As a fellow veteran ({sender_branch}), it's always great to see peers driving high-impact technical architectures in industry.

I recently architected an enterprise Lakehouse and vector telemetry pipeline on Databricks/PySpark (For Your Service platform) and am targeting the {role_label} team in {self.location}.

I'd appreciate the opportunity to connect, hear about your experience on the engineering team at {self.company}, and learn what capabilities the technical leadership prioritizes most.

Respectfully,
{sender_name}
{sender_branch}"""
        return message

    def generate_hiring_manager_outreach_message(
        self,
        manager_name: str = "[Manager Name]",
        sender_name: str = "Free Hall",
        sender_title: str = "Senior AI Data Engineer & Lakehouse Architect | Special Operations Veteran",
        target_role: Optional[str] = None
    ) -> str:
        """Generates an executive outreach message for Engineering Directors & Hiring Managers."""
        role_label = target_role or self.role
        message = f"""Hi {manager_name},

I am reaching out regarding the {role_label} opportunity with {self.company} in {self.location}. 

With 20+ years of operational leadership as a Special Forces Intelligence/Team Sergeant (18F/18Z) paired with proven lakehouse engineering execution (PySpark Medallion architectures, Databricks Unity Catalog governance, 384-dim tensor feature pipelines, and Kubernetes/Istio zero-trust deployments), my background maps directly to mission-critical telemetry and AI data infrastructure.

I deployed a live enterprise lakehouse platform at scale (240 unit tests passing, automated DLQ ingestion, and serverless control planes). I would welcome the chance for a brief technical discussion on how my telemetry pipeline and data governance background can accelerate your team's roadmap.

Live Lakehouse App: https://fys-matching-app-7474643734871839.aws.databricksapps.com/
GitHub Architecture: https://github.com/For-Your-Service/For-Your-Service

Best regards,
{sender_name}
{sender_title}"""
        return message


def get_curated_ge_aerospace_targets() -> List[Dict[str, Any]]:
    """Curated baseline of known aerospace engineering target roles and search vectors."""
    return [
        {
            "category": "Veteran Foot-in-the-Door (GE Aerospace Greenville)",
            "role": "Veterans in Engineering / Data / Leadership",
            "company": "GE Aerospace",
            "location": "Greenville, SC",
            "focus_areas": "Shared Service Bond, Engineering Teams, Data Infrastructure, Technical Leadership",
            "boolean_sample": 'site:linkedin.com/in ("GE Aerospace" OR "General Electric" OR "GE Aviation") ("Greenville" OR "Spartanburg" OR "South Carolina" OR "SC") ("Veteran" OR "Army" OR "Navy" OR "Air Force" OR "Marine" OR "Special Forces" OR "DoD" OR "Clearance") ("Engineer" OR "Data" OR "Manager" OR "Leader")'
        },
        {
            "category": "Data Engineering & Lakehouse",
            "role": "Senior AI Data Engineer",
            "company": "GE Aerospace",
            "location": "Greenville, SC / Remote",
            "focus_areas": "PySpark, Databricks Lakehouse, Delta Lake, Unity Catalog, Sensor Telemetry",
            "boolean_sample": 'site:linkedin.com/in ("GE Aerospace" OR "General Electric") ("Data Engineer" OR "AI Engineer") ("Greenville" OR "SC") ("Veteran" OR "Military" OR "Clearance")'
        },
        {
            "category": "AI / ML Infrastructure",
            "role": "Staff Machine Learning Engineer",
            "company": "GE Aerospace",
            "location": "Greenville, SC",
            "focus_areas": "Predictive Maintenance, Vibration Feature Stores, PyTorch, Real-Time Inference",
            "boolean_sample": 'site:linkedin.com/in ("GE Aerospace") ("Machine Learning" OR "MLOps") ("South Carolina" OR "Greenville") ("Veteran" OR "Army" OR "Navy" OR "Air Force")'
        },
        {
            "category": "Cloud & DevSecOps",
            "role": "Lead Cloud Infrastructure Architect",
            "company": "GE Aerospace",
            "location": "Greenville, SC",
            "focus_areas": "Terraform, AWS, Kubernetes, Istio Service Mesh, Zero-Trust Architecture",
            "boolean_sample": 'site:linkedin.com/in ("GE Aerospace") ("Cloud Architect" OR "DevOps" OR "Kubernetes") ("Greenville") ("Veteran" OR "Security Clearance")'
        }
    ]
