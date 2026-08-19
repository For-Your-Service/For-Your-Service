"""
Sample Data and Offline Fallback Engine
For Your Service - 7 Eagle Group
Provides realistic veteran-friendly job postings, fallback profiles, and local job matching.
100% Free - Works without external paid API or cloud requirements.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional

# Realistic veteran-friendly job postings
SAMPLE_JOBS: List[Dict] = [
    {
        "job_id": "fys_001",
        "title": "Lead Cloud Solutions Architect",
        "company": "Lockheed Martin",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC (Hybrid)",
        "salary_min": 145000,
        "salary_max": 185000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "USAJobs / Defense Partners",
        "description": "Lead enterprise cloud modernization using AWS, Kubernetes, Terraform, and Databricks. Design zero-trust data architectures and mission-critical pipelines. Prior military special operations or defense intelligence experience strongly valued.",
        "skills": ["aws", "kubernetes", "terraform", "python", "databricks", "docker", "ci/cd", "linux", "cloud architecture", "leadership"],
        "url": "https://www.lockheedmartinjobs.com"
    },
    {
        "job_id": "fys_002",
        "title": "Senior DevOps & Platform Engineer",
        "company": "Michelin North America",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 125000,
        "salary_max": 160000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "description": "Seeking experienced DevOps Engineer to architect automated CI/CD pipelines, Kubernetes clusters, and infrastructure-as-code deployments using Terraform and GitHub Actions. Strong military leadership and technical problem-solving background preferred.",
        "skills": ["devops", "kubernetes", "docker", "terraform", "python", "github actions", "bash", "ci/cd", "aws", "prometheus"],
        "url": "https://jobs.michelinman.com"
    },
    {
        "job_id": "fys_003",
        "title": "Senior Cyber Threat Intelligence Analyst",
        "company": "Booz Allen Hamilton",
        "city": "Columbia",
        "state": "SC",
        "location_display": "Columbia, SC / Remote",
        "salary_min": 115000,
        "salary_max": 150000,
        "clearance_required": "Top Secret / SCI",
        "veteran_friendly": True,
        "source": "JSearch API",
        "description": "Conduct all-source cyber threat intelligence analysis, threat actor profiling, and link analysis. Utilize Palantir, i2 Analyst's Notebook, and SIEM tools to deliver executive-level intelligence briefings to defense stakeholders.",
        "skills": ["cybersecurity", "threat intelligence", "palantir", "i2 analyst notebook", "link analysis", "siem", "python", "incident response", "executive briefings"],
        "url": "https://www.boozallen.com/careers"
    },
    {
        "job_id": "fys_004",
        "title": "Systems Administrator / Cloud Operations Lead",
        "company": "Fluor Corporation",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 95000,
        "salary_max": 130000,
        "clearance_required": "Public Trust",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "description": "Manage enterprise Windows/Linux server infrastructure, Active Directory, VMware virtualization, and Azure cloud resources. Support global engineering projects with high availability standards.",
        "skills": ["windows server", "active directory", "linux", "vmware", "azure", "powershell", "networking", "cisco", "troubleshooting"],
        "url": "https://www.fluor.com/careers"
    },
    {
        "job_id": "fys_005",
        "title": "Data Engineering Lead (Databricks / PySpark)",
        "company": "General Dynamics Information Technology",
        "city": "Charleston",
        "state": "SC",
        "location_display": "Charleston, SC (Remote Eligible)",
        "salary_min": 135000,
        "salary_max": 175000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "USAJobs",
        "description": "Design and optimize high-throughput data lakehouses using Databricks, Apache Spark, Delta Lake, and AWS. Build scalable ETL pipelines and vector search pipelines for defense applications.",
        "skills": ["databricks", "spark", "python", "sql", "delta lake", "aws", "data pipelines", "lakehouse", "etl", "git"],
        "url": "https://www.gdit.com/careers"
    },
    {
        "job_id": "fys_006",
        "title": "Operations & Logistics Program Manager",
        "company": "BMW Manufacturing Co.",
        "city": "Spartanburg",
        "state": "SC",
        "location_display": "Spartanburg, SC",
        "salary_min": 105000,
        "salary_max": 140000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "description": "Oversee complex supply chain operations, fleet management, and production line logistics. Military veterans with NCO/Officer operations management experience (11B, 88M, 92A, 18Z) highly encouraged to apply.",
        "skills": ["operations management", "supply chain", "logistics", "team leadership", "risk management", "continuous improvement", "sap", "excel"],
        "url": "https://www.bmwgroup.jobs"
    },
    {
        "job_id": "fys_007",
        "title": "Principal Cyber Security Engineer (Red Team / Penetration Testing)",
        "company": "Raytheon Technologies (RTX)",
        "city": "Tampa",
        "state": "FL",
        "location_display": "Tampa, FL / Remote",
        "salary_min": 150000,
        "salary_max": 195000,
        "clearance_required": "Top Secret / SCI",
        "veteran_friendly": True,
        "source": "Defense Partners",
        "description": "Perform adversary emulation, penetration testing, and security architecture reviews for defense networks. Hands-on experience with exploit development, Wireshark, Metasploit, and Linux kernel required.",
        "skills": ["cybersecurity", "penetration testing", "python", "metasploit", "wireshark", "linux", "reverse engineering", "security+", "cissp"],
        "url": "https://careers.rtx.com"
    },
    {
        "job_id": "fys_008",
        "title": "Senior Network Security Engineer",
        "company": "CACI International",
        "city": "Fayetteville",
        "state": "NC",
        "location_display": "Fayetteville, NC (Fort Liberty area)",
        "salary_min": 110000,
        "salary_max": 145000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "USAJobs",
        "description": "Design and maintain secure tactical and enterprise IP networks, Cisco routers/switches, firewalls, and SATCOM systems. Ideal for transitioning 25B, 18E, or Navy IT specialists.",
        "skills": ["cisco", "networking", "firewalls", "tcp/ip", "security+", "satcom", "voip", "active directory", "troubleshooting"],
        "url": "https://careers.caci.com"
    },
    {
        "job_id": "fys_009",
        "title": "Director of Field Operations & Mission Support",
        "company": "7 Eagle Group Partner Employer",
        "city": "Atlanta",
        "state": "GA",
        "location_display": "Atlanta, GA (Hybrid)",
        "salary_min": 140000,
        "salary_max": 180000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "7 Eagle Group Direct",
        "description": "Lead cross-functional technical field teams delivering enterprise infrastructure deployments. Requires seasoned military leadership (E-7+ or O-3+), strategic planning, and crisis decision-making.",
        "skills": ["executive leadership", "strategic planning", "operations management", "risk mitigation", "cross-functional teams", "budgeting", "crisis management"],
        "url": "https://7eaglegroup.com"
    },
    {
        "job_id": "fys_010",
        "title": "Clinical Operations Specialist / Healthcare Lead",
        "company": "Prisma Health",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 85000,
        "salary_max": 120000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "description": "Manage clinical workflows, emergency triage protocols, and healthcare documentation. Great fit for military medics (68W), Navy Hospital Corpsmen (HM), or Special Forces Medics (18D).",
        "skills": ["emergency care", "patient triage", "clinical operations", "emr", "healthcare administration", "team leadership", "critical decision making"],
        "url": "https://prismahealth.org/careers"
    }
]


# Demo Veteran Profile (William Free Hall - 18F / Solutions Architect)
DEMO_VETERAN_PROFILE = {
    "name": "William Free Hall",
    "email": "whall4.wh@gmail.com",
    "phone": "(910) 584-3843",
    "branch": "Army",
    "rank": "E-8 / Master Sergeant",
    "mos": "18F",
    "clearance": "Top Secret / SCI",
    "service_status": "Veteran (Retired)",
    "target_city": "Greenville",
    "target_state": "SC",
    "salary_min": 120000,
    "salary_max": 180000,
    "relocation": True,
    "remote_ok": True,
    "target_roles": ["Cloud Solutions Architect", "Data Engineer", "Technical Lead", "Intelligence Analyst"],
    "resume_text": """WILLIAM FREE HALL
Technical Lead & Solutions Architect | Cloud & Data Engineer
Niceville, FL  •  (910) 584-3843  •  whall4.wh@gmail.com  •  linkedin.com/in/william-free-hall  •  github.com/For-Your-Service

EXECUTIVE SUMMARY
Results-driven Technical Lead and Cloud/Data Architect with over 10 years of specialized experience in data analytics, data engineering, and executive intelligence briefings, backed by over 20 years of elite military leadership in US Army Special Operations. Proven track record of architecting multi-tier data lakehouses on Databricks, engineering graph analytical models, managing enterprise cloud infrastructure, and interpreting high-stakes intelligence analysis using Palantir and i2 Analyst's Notebook for General Officers and senior DOD decision-makers. Combines operational discipline with deep technical expertise in PySpark, Databricks, Terraform, Kubernetes, and CI/CD pipelines to deliver high-availability, cost-optimized enterprise platforms.

TECHNICAL SKILLS
• Data & Analytics Engineering: Palantir, i2 Analyst's Notebook, Databricks, Apache Spark (PySpark), Delta Lake, Unity Catalog, Vector Search, PyTorch, Transformers, Scikit-Learn, Pandas, NumPy
• Cloud & Infrastructure: AWS (Lambda, EC2, S3, IAM, CloudFormation), GCP (Cloud Functions, GCS, GKE), Azure (VMs, AKS), Serverless Architecture
• Containers & Orchestration: Kubernetes (GKE, AKS), Docker, Helm
• IaC & DevOps: Terraform, GitHub Actions, Jenkins, GitLab CI, Git, Bash/Shell Scripting
• Databases & Query Languages: SQL (Databricks SQL, PostgreSQL), Vector Databases, Graph & Link Analysis
• Executive Communication & Ops: Executive Data Briefings (General Officer Level), Inter-Agency Coordination (DOD, CIA, State Dept), Cross-Functional Team Leadership, Process Optimization

PROFESSIONAL EXPERIENCE
Technical Lead & Solutions Architect | For Your Service (2024 – Present)
Partnered with 7 Eagle Group (Veteran Placement Organization)
• Cloud & Data Lakehouse Architecture: Architected an enterprise multi-tier data lakehouse (Bronze / Silver / Gold) on Databricks utilizing Unity Catalog for end-to-end data governance.
• Machine Learning & ETL Engineering: Engineered automated ETL pipelines in PySpark ingesting and processing 670+ live job market postings from external REST APIs (USAJobs, Adzuna).
• Neural Network & Semantic Search: Built a Siamese twin-tower neural network utilizing 384-dimensional vector embeddings for high-precision semantic job-to-candidate matching.
• DevOps & Infrastructure as Code: Implemented automated CI/CD deployment pipelines using GitHub Actions and managed infrastructure state using Terraform.

Cloud Engineer & DevOps Analyst | ConocoPhillips (2022 – 2024)
• Enterprise Cloud & Pipeline Automation: Architected and maintained automated CI/CD deployment pipelines across multi-tenant cloud environments.
• Infrastructure as Code (IaC): Provisioned and managed cloud infrastructure using Terraform, standardizing multi-environment configurations.

Special Forces Intelligence Sergeant (18F) & Team Sergeant | U.S. Army Special Forces (1999 – 2017)
• Executive Briefings & Strategic Decision Support: Synthesized complex analytics into high-impact operational briefings directly to General Officers.
• Data Analytics & Link Analysis: Utilized Palantir and i2 Analyst's Notebook to aggregate, fuse, and analyze massive multi-source datasets, identifying complex relational networks and actionable intelligence.
• Inter-Agency Coordination: Planned and executed sensitive operations requiring detailed intelligence analysis in coordination with inter-agency partners (DOD, CIA, State Dept).

EDUCATION & CERTIFICATIONS
• Bachelor of Science in Cybersecurity
• AWS Certified Cloud Practitioner
• U.S. Army Special Forces Qualification Course (SFQC) – 18F Intelligence Sergeant & 18 Series Green Beret
"""
}


def load_cached_scraped_jobs() -> List[Dict]:
    """
    Attempt to load real scraped jobs from repo results directory.
    Falls back to SAMPLE_JOBS if no files found.
    """
    repo_root = Path(__file__).resolve().parent.parent
    results_dir = repo_root / "results"
    
    if results_dir.exists():
        json_files = list(results_dir.glob("scraped_jobs_*.json"))
        if json_files:
            latest_file = max(json_files, key=os.path.getmtime)
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    raw_jobs = json.load(f)
                    
                parsed_jobs = []
                for j in raw_jobs:
                    # Normalize fields
                    loc = j.get("location", {})
                    salary = j.get("salary", {})
                    
                    parsed_jobs.append({
                        "job_id": str(j.get("job_id", "")),
                        "title": j.get("title", "Unknown Title"),
                        "company": j.get("company", "Company"),
                        "city": loc.get("city", "Greenville"),
                        "state": loc.get("state", "SC"),
                        "location_display": loc.get("display", f"{loc.get('city', '')}, {loc.get('state', '')}"),
                        "salary_min": float(salary.get("min", 60000) or 60000),
                        "salary_max": float(salary.get("max", 120000) or 120000),
                        "clearance_required": "None",
                        "veteran_friendly": True,
                        "source": j.get("source", "Adzuna API"),
                        "description": j.get("description", ""),
                        "skills": [w.strip() for w in j.get("title", "").lower().split() if len(w) > 3],
                        "url": j.get("url", "https://adzuna.com")
                    })
                
                if parsed_jobs:
                    # Combine with curated sample jobs for rich experience
                    return SAMPLE_JOBS + parsed_jobs
            except Exception:
                pass

    return SAMPLE_JOBS
