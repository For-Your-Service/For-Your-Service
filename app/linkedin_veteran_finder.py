#!/usr/bin/env python3
"""
File: app/linkedin_veteran_finder.py
Description: LinkedIn Veteran Talent & Peer Discovery Engine for Aerospace & Defense AI Data Engineers.
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Gunslinger Clean-Core
"""

import urllib.parse
import json
import re
from typing import List, Dict, Any, Optional

DEFAULT_COMPANIES = [
    "GE Aerospace",
    "General Electric",
    "Lockheed Martin",
    "Boeing",
    "Pratt & Whitney",
    "Raytheon Technologies",
    "Northrop Grumman",
    "L3Harris",
    "General Dynamics"
]

DEFAULT_ROLES = [
    "Sr AI Data Engineer",
    "Senior AI Data Engineer",
    "Staff Data Engineer",
    "AI Data Architect",
    "Machine Learning Engineer",
    "Databricks Lakehouse Architect",
    "Cloud Infrastructure Engineer",
    "Principal Data Engineer"
]

DEFAULT_LOCATIONS = [
    "Greenville, SC",
    "Greenville-Spartanburg-Anderson, SC",
    "South Carolina",
    "Remote",
    "Huntsville, AL",
    "Atlanta, GA",
    "Washington DC"
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


class LinkedInVeteranFinder:
    """
    Generates precision Boolean search queries, direct LinkedIn URLs,
    and automated peer outreach templates for veteran technical talent.
    """

    def __init__(
        self,
        company: str = "GE Aerospace",
        role: str = "Sr AI Data Engineer",
        location: str = "Greenville, SC",
        branch_filter: Optional[str] = None
    ):
        self.company = company
        self.role = role
        self.location = location
        self.branch_filter = branch_filter

    def generate_boolean_query(self) -> str:
        """
        Builds a Google/Bing X-Ray Boolean query targeting indexed LinkedIn profiles.
        Example: site:linkedin.com/in ("GE Aerospace" OR "General Electric") ("Sr AI Data Engineer" OR "Data Engineer") ("Greenville" OR "SC") ("Veteran" OR "Army" OR ...)
        """
        # Company clause
        if "GE" in self.company or "General Electric" in self.company:
            company_clause = '("GE Aerospace" OR "General Electric" OR "GE Aviation")'
        else:
            company_clause = f'"{self.company}"'

        # Role clause
        clean_role = self.role.replace("Sr", "Senior").replace("Senior", "")
        role_clause = f'("{self.role}" OR "AI Data Engineer" OR "Data Engineer" OR "Lakehouse" OR "PySpark")'

        # Location clause
        if "Greenville" in self.location:
            loc_clause = '("Greenville" OR "Spartanburg" OR "South Carolina" OR "SC")'
        elif "Remote" in self.location:
            loc_clause = '("Remote" OR "United States")'
        else:
            loc_clause = f'"{self.location}"'

        # Military background clause
        if self.branch_filter and self.branch_filter != "All":
            military_clause = f'("{self.branch_filter}" OR "Veteran" OR "Military")'
        else:
            military_clause = '("Veteran" OR "Army" OR "Navy" OR "Air Force" OR "Marine" OR "Special Forces" OR "DoD" OR "Clearance")'

        query = f'site:linkedin.com/in {company_clause} {role_clause} {loc_clause} {military_clause}'
        return query

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
        keywords = f"{self.company} {self.role} Veteran {self.location}"
        encoded = urllib.parse.quote_plus(keywords)
        return f"https://www.linkedin.com/search/results/people/?keywords={encoded}&origin=GLOBAL_SEARCH_HEADER"

    def generate_peer_outreach_message(
        self,
        peer_name: str = "[First Name]",
        sender_name: str = "Free Hall",
        sender_branch: str = "US Army Special Forces (18F / 18Z, Ret.)",
        target_role: str = "Sr AI Data Engineer"
    ) -> str:
        """
        Generates a warm, professional veteran-to-veteran peer connection message.
        """
        message = f"""Hi {peer_name},

I saw your profile and noticed your transition from military service to engineering at {self.company}. As a fellow veteran ({sender_branch}), it's always great to see peers driving high-impact technical architectures in aerospace and defense.

I recently architected an enterprise Lakehouse and vector telemetry pipeline on Databricks/PySpark (For Your Service platform) and am targeting the {target_role} team in {self.location}.

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
        target_role: str = "Sr AI Data Engineer"
    ) -> str:
        """
        Generates an executive outreach message for Engineering Directors & Hiring Managers at GE Aerospace.
        """
        message = f"""Hi {manager_name},

I am reaching out regarding the {target_role} opportunity with {self.company} in {self.location}. 

With 20+ years of operational leadership as a Special Forces Intelligence/Team Sergeant (18F/18Z) paired with proven lakehouse engineering execution (PySpark Medallion architectures, Databricks Unity Catalog governance, 384-dim tensor feature pipelines, and Kubernetes/Istio zero-trust deployments), my background maps directly to mission-critical aerospace telemetry and AI data infrastructure.

I deployed a live enterprise lakehouse platform at scale (232 unit tests passing, automated DLQ ingestion, and serverless control planes). I would welcome the chance for a brief technical discussion on how my telemetry pipeline and data governance background can accelerate your team's roadmap.

Live Lakehouse App: https://fys-matching-app-7474643734871839.aws.databricksapps.com/
GitHub Architecture: https://github.com/For-Your-Service/For-Your-Service

Best regards,
{sender_name}
{sender_title}"""
        return message


def get_curated_ge_aerospace_targets() -> List[Dict[str, Any]]:
    """
    Curated baseline of known aerospace engineering target roles and search vectors
    for GE Aerospace in the Greenville / Upstate SC defense corridor.
    """
    return [
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
        },
        {
            "category": "Engineering Leadership & Talent",
            "role": "Director of AI & Data Platform Engineering / Talent Acquisition",
            "company": "GE Aerospace",
            "location": "Greenville, SC / Cincinnati, OH",
            "focus_areas": "Engineering Hiring, Platform Modernization, Veteran Recruitment Programs",
            "boolean_sample": 'site:linkedin.com/in ("GE Aerospace") ("Engineering Manager" OR "Director" OR "Technical Recruiter") ("Data" OR "AI") ("Veteran" OR "Military")'
        }
    ]
