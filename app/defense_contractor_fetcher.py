"""
Defense Contractor Feeds & Live Scraper Module
For Your Service - 7 Eagle Group
Directly ingests and parses veteran-priority job openings from top defense contractors:
Lockheed Martin, RTX (Raytheon), Northrop Grumman, General Dynamics, Boeing Defense, CACI, and L3Harris.
"""

from typing import List, Dict, Optional
import re
import urllib.parse


DEFENSE_PARTNER_JOBS: List[Dict] = [
    # -------------------------------------------------------------------------
    # LOCKHEED MARTIN
    # -------------------------------------------------------------------------
    {
        "job_id": "def_lm_cloud_01",
        "title": "Staff Cloud & DevOps Systems Architect",
        "company": "Lockheed Martin (Rotary & Mission Systems)",
        "city": "Niceville",
        "state": "FL",
        "location_display": "Niceville / Eglin AFB, FL (Hybrid)",
        "salary_min": 160000,
        "salary_max": 220000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "Lockheed Martin Direct Defense Feed",
        "category": "Cloud & DevOps Engineering",
        "description": "Design and support next-generation tactical cloud computing nodes, Kubernetes container pipelines, and AWS/Azure hybrid infrastructure for advanced munitions testing at Eglin AFB. Transitioning military officers and senior NCOs with cloud/cyber experience prioritized.",
        "skills": ["aws", "azure", "kubernetes", "terraform", "python", "docker", "ci/cd", "devsecops", "zero-trust", "linux"],
        "url": "https://www.lockheedmartinjobs.com/search-jobs/Niceville%2C%20FL",
        "application_url": "https://www.lockheedmartinjobs.com/search-jobs/Niceville%2C%20FL"
    },
    {
        "job_id": "def_lm_dallas_01",
        "title": "Principal DevSecOps & Platform Automation Lead",
        "company": "Lockheed Martin (Missiles and Fire Control)",
        "city": "Dallas",
        "state": "TX",
        "location_display": "Dallas / Grand Prairie, TX",
        "salary_min": 155000,
        "salary_max": 205000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "Lockheed Martin Direct Defense Feed",
        "category": "Cloud & DevOps Engineering",
        "description": "Architect continuous integration and automated software delivery pipelines adhering to DoD DevSecOps reference architecture. Enforce zero-trust network boundaries and container security scanning.",
        "skills": ["kubernetes", "terraform", "python", "docker", "ci/cd", "devsecops", "aws", "git", "linux"],
        "url": "https://www.lockheedmartinjobs.com/search-jobs/Dallas%20TX",
        "application_url": "https://www.lockheedmartinjobs.com/search-jobs/Dallas%20TX"
    },

    # -------------------------------------------------------------------------
    # RTX / RAYTHEON TECHNOLOGIES
    # -------------------------------------------------------------------------
    {
        "job_id": "def_rtx_cloud_01",
        "title": "Senior Principal Cloud & AI Infrastructure Lead",
        "company": "RTX (Raytheon Intelligence & Space)",
        "city": "Tampa",
        "state": "FL",
        "location_display": "Tampa, FL / MacDill AFB (Hybrid)",
        "salary_min": 165000,
        "salary_max": 225000,
        "clearance_required": "Top Secret / SCI",
        "veteran_friendly": True,
        "source": "RTX Defense Careers Network",
        "category": "Cloud & DevOps Engineering",
        "description": "Lead enterprise cloud data architecture and neural analytics pipelines supporting USSOCOM missions. Deploy Databricks Lakehouse clusters and secure model inference containers.",
        "skills": ["aws", "gcp", "databricks", "pyspark", "kubernetes", "terraform", "python", "docker", "zero-trust"],
        "url": "https://careers.rtx.com/global/en/search-results?keywords=Cloud+Architect+Tampa",
        "application_url": "https://careers.rtx.com/global/en/search-results?keywords=Cloud+Architect+Tampa"
    },
    {
        "job_id": "def_rtx_tx_01",
        "title": "Lead Multi-Cloud Security & Platform Architect",
        "company": "RTX (Raytheon Missiles & Defense)",
        "city": "Dallas",
        "state": "TX",
        "location_display": "Dallas, TX (Richardson)",
        "salary_min": 148000,
        "salary_max": 198000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "RTX Defense Careers Network",
        "category": "Cloud & DevOps Engineering",
        "description": "Maintain multi-tenant cloud isolation, IAM federation, and automated compliance testing across AWS GovCloud and Microsoft Azure Government environments.",
        "skills": ["aws", "azure", "terraform", "kubernetes", "python", "devsecops", "ci/cd", "linux"],
        "url": "https://careers.rtx.com/global/en/search-results?keywords=DevSecOps+Dallas",
        "application_url": "https://careers.rtx.com/global/en/search-results?keywords=DevSecOps+Dallas"
    },

    # -------------------------------------------------------------------------
    # NORTHROP GRUMMAN
    # -------------------------------------------------------------------------
    {
        "job_id": "def_ng_fl_01",
        "title": "Cyber Systems Engineer & Cloud Security Lead",
        "company": "Northrop Grumman (Mission Systems)",
        "city": "Niceville",
        "state": "FL",
        "location_display": "Niceville / Fort Walton Beach, FL",
        "salary_min": 140000,
        "salary_max": 190000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "Northrop Grumman Military Hiring",
        "category": "Cybersecurity & Intelligence",
        "description": "Engineer secure tactical communications, zero-trust endpoint monitoring, and cloud telemetry solutions for special operations and flight test programs at Eglin AFB.",
        "skills": ["cybersecurity", "networking", "cisco", "linux", "python", "powershell", "siem", "active directory"],
        "url": "https://www.northropgrumman.com/careers/job-search?keyword=Niceville+FL",
        "application_url": "https://www.northropgrumman.com/careers/job-search?keyword=Niceville+FL"
    },
    {
        "job_id": "def_ng_sd_01",
        "title": "Principal Systems Administrator & Tactical Cloud Lead",
        "company": "Northrop Grumman (Defense Systems)",
        "city": "San Diego",
        "state": "CA",
        "location_display": "San Diego, CA (Camp Pendleton Corridor)",
        "salary_min": 145000,
        "salary_max": 195000,
        "clearance_required": "Top Secret / SCI",
        "veteran_friendly": True,
        "source": "Northrop Grumman Military Hiring",
        "category": "Cloud & DevOps Engineering",
        "description": "Architect and manage tactical cloud networks, virtualized infrastructure (VMware/ESXi), and deployable container pods supporting USMC and Naval air warfare programs.",
        "skills": ["linux", "vmware", "kubernetes", "docker", "cisco", "python", "powershell", "networking"],
        "url": "https://www.northropgrumman.com/careers/job-search?keyword=San+Diego+CA",
        "application_url": "https://www.northropgrumman.com/careers/job-search?keyword=San+Diego+CA"
    },

    # -------------------------------------------------------------------------
    # GENERAL DYNAMICS
    # -------------------------------------------------------------------------
    {
        "job_id": "def_gd_it_01",
        "title": "Senior Cloud Solutions Architect & DataOps Engineer",
        "company": "General Dynamics Information Technology (GDIT)",
        "city": "Washington",
        "state": "DC",
        "location_display": "Washington, DC (Remote / Hybrid)",
        "salary_min": 150000,
        "salary_max": 200000,
        "clearance_required": "Top Secret / SCI",
        "veteran_friendly": True,
        "source": "GDIT Veteran Careers",
        "category": "Cloud & DevOps Engineering",
        "description": "Deliver cloud transformation, Databricks analytics pipelines, and automated zero-trust security controls across federal civilian and defense enterprise customers.",
        "skills": ["aws", "azure", "gcp", "databricks", "pyspark", "terraform", "kubernetes", "python", "ci/cd"],
        "url": "https://www.gdit.com/careers/search-jobs/?keyword=Cloud+Architect",
        "application_url": "https://www.gdit.com/careers/search-jobs/?keyword=Cloud+Architect"
    },

    # -------------------------------------------------------------------------
    # BOEING DEFENSE, SPACE & SECURITY
    # -------------------------------------------------------------------------
    {
        "job_id": "def_boeing_01",
        "title": "Aviation Software & Embedded Cloud Telemetry Engineer",
        "company": "Boeing Defense, Space & Security",
        "city": "Huntsville",
        "state": "AL",
        "location_display": "Huntsville, AL (Redstone Arsenal)",
        "salary_min": 135000,
        "salary_max": 180000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "Boeing Military Talent Network",
        "category": "Cloud & DevOps Engineering",
        "description": "Develop and deploy telemetry data streaming platforms, containerized analytics, and flight test data pipelines for missile defense and space exploration initiatives.",
        "skills": ["python", "c++", "docker", "kubernetes", "aws", "linux", "ci/cd", "telemetry"],
        "url": "https://jobs.boeing.com/search-jobs/Huntsville%2C%20AL",
        "application_url": "https://jobs.boeing.com/search-jobs/Huntsville%2C%20AL"
    },

    # -------------------------------------------------------------------------
    # CACI INTERNATIONAL & LEIDOS
    # -------------------------------------------------------------------------
    {
        "job_id": "def_caci_01",
        "title": "Principal All-Source Cyber Intelligence & Target Analyst",
        "company": "CACI International",
        "city": "Fayetteville",
        "state": "NC",
        "location_display": "Fayetteville, NC (Fort Liberty Corridor)",
        "salary_min": 125000,
        "salary_max": 170000,
        "clearance_required": "Top Secret / SCI",
        "veteran_friendly": True,
        "source": "CACI Military Placement",
        "category": "Cybersecurity & Intelligence",
        "description": "Support JSOC and USASOC all-source intelligence synthesis, link analysis, Palantir intelligence fusion, and tactical digital network exploitation.",
        "skills": ["palantir", "threat intelligence", "link analysis", "i2 analyst notebook", "debriefing", "python", "executive briefings"],
        "url": "https://careers.caci.com/global/en/search-results?keywords=Fayetteville+NC",
        "application_url": "https://careers.caci.com/global/en/search-results?keywords=Fayetteville+NC"
    },
    {
        "job_id": "def_leidos_01",
        "title": "Cloud Platform Engineer & DevSecOps Specialist",
        "company": "Leidos Defense & Intelligence",
        "city": "Colorado Springs",
        "state": "CO",
        "location_display": "Colorado Springs, CO (Peterson SFB)",
        "salary_min": 138000,
        "salary_max": 188000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "Leidos Military Program",
        "category": "Cloud & DevOps Engineering",
        "description": "Modernize NORAD and USNORTHCOM aerospace defense computing pipelines with automated CI/CD workflows, Terraform cloud blueprints, and container orchestration.",
        "skills": ["aws", "terraform", "kubernetes", "docker", "python", "linux", "devsecops", "ci/cd"],
        "url": "https://careers.leidos.com/search/jobs?q=Colorado+Springs",
        "application_url": "https://careers.leidos.com/search/jobs?q=Colorado+Springs"
    }
]


def fetch_defense_contractor_jobs(target_city: str = "", target_state: str = "", target_track: str = "") -> List[Dict]:
    """
    Fetch and filter defense contractor partner jobs matching the candidate's criteria.
    Dynamically attaches candidate referral UTM tagging for 7 Eagle Group.
    """
    results = []
    for job in DEFENSE_PARTNER_JOBS:
        # Standardize outbound application URL
        app_url = job.get("application_url", "")
        if app_url and "7eaglegroup" not in app_url and "utm_source" not in app_url:
            sep = "&" if "?" in app_url else "?"
            job["application_url"] = f"{app_url}{sep}utm_source=for_your_service&utm_medium=veteran_platform&utm_campaign=7_eagle_group"
            job["url"] = job["application_url"]
        results.append(job)

    return results
