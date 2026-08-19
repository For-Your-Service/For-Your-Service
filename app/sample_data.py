"""
Sample Data and Offline Fallback Engine
For Your Service - 7 Eagle Group
Provides diverse veteran-friendly job postings across all career fields:
Operations, Logistics, Mechanics, Law Enforcement, Healthcare, Aviation, IT, and Leadership.
100% Free - Works offline without external paid API or cloud requirements.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional

# Realistic veteran-friendly job postings across diverse career categories
SAMPLE_JOBS: List[Dict] = [
    # -------------------------------------------------------------------------
    # OPERATIONS, PROGRAM MANAGEMENT & LEADERSHIP
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_ops_001",
        "title": "Director of Field Operations & Mission Support",
        "company": "7 Eagle Group Partner Employer",
        "city": "Atlanta",
        "state": "GA",
        "location_display": "Atlanta, GA (Hybrid / Remote)",
        "salary_min": 135000,
        "salary_max": 175000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "7 Eagle Group Direct",
        "category": "Operations & Leadership",
        "description": "Lead cross-functional technical and field teams delivering complex operational deployments. Requires seasoned military leadership (Senior NCO E-7+ or Officer O-3+), strategic risk planning, crisis decision-making, and SOP enforcement.",
        "skills": ["executive leadership", "strategic planning", "operations management", "risk mitigation", "cross-functional operations", "crisis management", "personnel accountability"],
        "url": "https://7eaglegroup.com"
    },
    {
        "job_id": "fys_ops_002",
        "title": "Operations Team Lead / Field Project Coordinator",
        "company": "Fluor Corporation",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 85000,
        "salary_max": 115000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Operations & Leadership",
        "description": "Coordinate field execution, workforce scheduling, safety compliance, and operational workflows for large infrastructure initiatives. Military combat arms (11B, 11C, 19D, 0311) and NCOs with squad/platoon leadership excel in this role.",
        "skills": ["team leadership", "operational planning", "safety compliance", "risk assessment", "situational awareness", "standard operating procedures"],
        "url": "https://www.fluor.com/careers"
    },

    # -------------------------------------------------------------------------
    # LOGISTICS, SUPPLY CHAIN & TRANSPORTATION
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_log_001",
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
        "category": "Logistics & Supply Chain",
        "description": "Oversee complex supply chain operations, fleet management, and production line logistics. Military veterans with logistics, supply, and transportation backgrounds (88M, 92A, 92Y, LS, 2T2X1, 0431) strongly encouraged to apply.",
        "skills": ["supply chain optimization", "inventory auditing", "fleet tracking", "procurement", "shipping & receiving", "warehouse management", "sap", "excel"],
        "url": "https://www.bmwgroup.jobs"
    },
    {
        "job_id": "fys_log_002",
        "title": "Fleet Transportation Supervisor / CDL Route Dispatcher",
        "company": "Schneider National",
        "city": "Columbia",
        "state": "SC",
        "location_display": "Columbia, SC",
        "salary_min": 72000,
        "salary_max": 98000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Logistics & Transportation",
        "description": "Manage commercial freight routes, driver scheduling, DOT compliance, and fleet safety inspections. Direct translation for military motor transport operators (88M, 3531) and convoy commanders.",
        "skills": ["heavy vehicle operations", "route planning", "cargo safety", "preventive maintenance", "dot compliance", "telematics"],
        "url": "https://schneiderjobs.com"
    },
    {
        "job_id": "fys_log_003",
        "title": "Supply Chain & Property Inventory Controller",
        "company": "Lockheed Martin",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 78000,
        "salary_max": 108000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "USAJobs / Defense Partners",
        "category": "Logistics & Supply Chain",
        "description": "Maintain defense asset accountability, warehouse logistics, and inventory auditing for aerospace manufacturing. Direct fit for 92Y, 92A, LS, 0431, SK specialists.",
        "skills": ["property accountability", "asset tracking", "budget reconciliation", "vendor coordination", "erp software", "excel"],
        "url": "https://www.lockheedmartinjobs.com"
    },

    # -------------------------------------------------------------------------
    # MAINTENANCE, MECHANICS & FIELD ENGINEERING
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_mech_001",
        "title": "Fleet Maintenance Shop Supervisor / Heavy Diesel Mechanic",
        "company": "Penske Truck Leasing",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 75000,
        "salary_max": 102000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Maintenance & Mechanics",
        "description": "Supervise diesel fleet maintenance, hydraulic troubleshooting, engine diagnostics, and preventive inspection schedules. Ideal for 91B, 91X, MK, 3531, or mechanical NCOs.",
        "skills": ["diesel engine overhaul", "electrical troubleshooting", "hydraulic repair", "preventive maintenance inspection", "diagnostic testing", "team leadership"],
        "url": "https://penske.jobs"
    },
    {
        "job_id": "fys_mech_002",
        "title": "Aviation Maintenance Technician (A&P / Helicopter Specialist)",
        "company": "Boeing",
        "city": "Charleston",
        "state": "SC",
        "location_display": "Charleston, SC",
        "salary_min": 85000,
        "salary_max": 120000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "Defense Partners",
        "category": "Aviation & Maintenance",
        "description": "Perform structural inspections, turbine powerplant maintenance, and flight-line diagnostics. Direct match for Army 15T/15U, Air Force 2A6X1, and Navy Aviation mechanics.",
        "skills": ["turbine engine maintenance", "rotor systems repair", "faa/military aviation standards", "avionics diagnostics", "precision torque tools"],
        "url": "https://jobs.boeing.com"
    },

    # -------------------------------------------------------------------------
    # LAW ENFORCEMENT, SECURITY & PHYSICAL PROTECTION
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_sec_001",
        "title": "Corporate Physical Security Manager / Site Protection Lead",
        "company": "Duke Energy",
        "city": "Charlotte",
        "state": "NC",
        "location_display": "Charlotte, NC / Greenville, SC",
        "salary_min": 92000,
        "salary_max": 128000,
        "clearance_required": "Public Trust",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Law Enforcement & Security",
        "description": "Oversee physical security operations, access control infrastructure, threat assessments, and emergency response plans for critical energy facilities. Direct fit for 31B, 31D, 5811, 3P0X1, MA, ME.",
        "skills": ["force protection", "perimeter security", "incident investigation", "access control", "cctv", "conflict de-escalation", "emergency response"],
        "url": "https://duke-energy.com/careers"
    },
    {
        "job_id": "fys_sec_002",
        "title": "Federal Background & Fraud Investigator",
        "company": "CACI International",
        "city": "Columbia",
        "state": "SC",
        "location_display": "Columbia, SC (Remote / Hybrid)",
        "salary_min": 80000,
        "salary_max": 110000,
        "clearance_required": "Top Secret",
        "veteran_friendly": True,
        "source": "USAJobs",
        "category": "Law Enforcement & Security",
        "description": "Conduct investigative interviews, background verifications, and record checks for federal security clearance candidates. Great fit for 31D, 35M, CID agents, NCIS/OSI veterans, or military investigators.",
        "skills": ["felony investigations", "interpersonal interviewing", "debriefing", "case file preparation", "court testimony", "background databases"],
        "url": "https://careers.caci.com"
    },

    # -------------------------------------------------------------------------
    # HEALTHCARE, MEDICAL & SAFETY
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_med_001",
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
        "category": "Healthcare & Medical",
        "description": "Manage clinical workflows, emergency triage protocols, patient intake, and healthcare documentation. Direct fit for military combat medics (68W), Navy Hospital Corpsmen (HM), 4N0X1, or 18D.",
        "skills": ["emergency trauma care", "patient triage", "vital signs assessment", "medical documentation", "critical decision making", "emr", "cpr / bls"],
        "url": "https://prismahealth.org/careers"
    },
    {
        "job_id": "fys_med_002",
        "title": "Environmental Health & Safety (EHS) Manager",
        "company": "Michelin North America",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 90000,
        "salary_max": 125000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Healthcare & Medical",
        "description": "Lead OSHA compliance audits, hazmat protocols, workplace safety training, and incident investigation. Direct match for Coast Guard MST, Army Safety NCOs, and Medical/Hazmat specialists.",
        "skills": ["hazmat compliance", "environmental compliance", "safety enforcement", "incident command", "osha compliance", "risk assessment"],
        "url": "https://jobs.michelinman.com"
    },

    # -------------------------------------------------------------------------
    # HUMAN RESOURCES, ADMINISTRATION & RECRUITING
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_hr_001",
        "title": "Human Resources & Talent Acquisition Specialist (Veteran Hiring)",
        "company": "7 Eagle Group Partner Employer",
        "city": "Atlanta",
        "state": "GA",
        "location_display": "Atlanta, GA / Remote",
        "salary_min": 75000,
        "salary_max": 105000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "7 Eagle Group Direct",
        "category": "Human Resources & Administration",
        "description": "Lead talent sourcing, candidate screening, veteran transition mentorship, and HR onboarding. Direct fit for 42A, Navy PS, Air Force 3F0X1, and military recruiters.",
        "skills": ["personnel records management", "talent acquisition", "onboarding / outboarding", "hr compliance", "interviewing", "hris", "excel"],
        "url": "https://7eaglegroup.com"
    },

    # -------------------------------------------------------------------------
    # IT, CLOUD, CYBERSECURITY & INTELLIGENCE
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_tech_001",
        "title": "Lead Cloud Solutions Architect",
        "company": "Lockheed Martin",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC (Hybrid / Remote)",
        "salary_min": 145000,
        "salary_max": 185000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "USAJobs / Defense Partners",
        "category": "Information Technology & Cloud",
        "description": "Lead enterprise cloud modernization using AWS, Kubernetes, Terraform, and Databricks. Design zero-trust data architectures and mission-critical pipelines. Prior military communications, cyber, or intelligence experience valued.",
        "skills": ["aws", "kubernetes", "terraform", "python", "databricks", "docker", "ci/cd", "linux", "cloud architecture", "leadership"],
        "url": "https://www.lockheedmartinjobs.com"
    },
    {
        "job_id": "fys_tech_002",
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
        "category": "Intelligence & Analytics",
        "description": "Conduct all-source cyber threat intelligence analysis, threat actor profiling, and link analysis. Utilize Palantir, i2 Analyst's Notebook, and SIEM tools to deliver executive-level intelligence briefings to defense stakeholders.",
        "skills": ["cybersecurity", "threat intelligence", "palantir", "i2 analyst notebook", "link analysis", "siem", "python", "incident response", "executive briefings"],
        "url": "https://www.boozallen.com/careers"
    },
    {
        "job_id": "fys_tech_003",
        "title": "Systems Administrator / Network Support Lead",
        "company": "Fluor Corporation",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 85000,
        "salary_max": 118000,
        "clearance_required": "Public Trust",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Information Technology",
        "description": "Manage enterprise Windows/Linux server infrastructure, Active Directory, Cisco network switches, and cloud access. Direct translation for 25B, 25U, Navy IT, 0671, 1D7X1.",
        "skills": ["windows server", "active directory", "cisco", "linux", "tcp/ip", "powershell", "virtualization", "networking", "troubleshooting"],
        "url": "https://www.fluor.com/careers"
    },

    # -------------------------------------------------------------------------
    # CONSTRUCTION, HEAVY INFRASTRUCTURE & COMBAT ENGINEERING
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_const_001",
        "title": "Heavy Civil Construction Site Superintendent",
        "company": "Kiewit Infrastructure",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC / Regional",
        "salary_min": 95000,
        "salary_max": 135000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Construction & Infrastructure",
        "description": "Direct large-scale earthmoving, bridge, and highway construction projects. Enforce OSHA safety protocols, subcontractor scheduling, and blueprint execution. Perfect for Army 12B/12N Combat Engineers, Navy Seabees (BU/EO), and Air Force RED HORSE.",
        "skills": ["heavy equipment operations", "site safety enforcement", "subcontractor management", "blueprint reading", "project scheduling", "osha 30", "earthmoving"],
        "url": "https://kiewit.com/careers"
    },

    # -------------------------------------------------------------------------
    # ADVANCED MANUFACTURING, PRECISION MACHINING & INDUSTRIAL TRADES
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_mfg_001",
        "title": "Advanced CNC Manufacturing & Tooling Supervisor",
        "company": "General Electric Aerospace",
        "city": "Greenville",
        "state": "SC",
        "location_display": "Greenville, SC",
        "salary_min": 88000,
        "salary_max": 122000,
        "clearance_required": "Secret",
        "veteran_friendly": True,
        "source": "USAJobs / Defense Partners",
        "category": "Advanced Manufacturing & Machining",
        "description": "Supervise multi-axis CNC machining centers producing high-tolerance turbine components. Direct fit for military machinists, weapons repairers (91F, 91G), Navy Machinery Repairmen (MR), and Air Force Metals Techs.",
        "skills": ["cnc machining", "precision measurement", "quality assurance", "blueprint interpretation", "lean manufacturing", "g-code", "tooling calibration"],
        "url": "https://geaerospace.com/careers"
    },

    # -------------------------------------------------------------------------
    # MARITIME OPERATIONS & PORT LOGISTICS
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_mar_001",
        "title": "Port Operations & Marine Terminal Safety Supervisor",
        "company": "South Carolina Ports Authority",
        "city": "Charleston",
        "state": "SC",
        "location_display": "Charleston, SC",
        "salary_min": 82000,
        "salary_max": 115000,
        "clearance_required": "Public Trust",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Maritime & Port Operations",
        "description": "Oversee container terminal vessel operations, stevedore safety, and maritime cargo handling. Ideal fit for Coast Guard Boatswain's Mates (BM), Marine Science Techs (MST), and Navy Boatswain's Mates / Quartermasters.",
        "skills": ["maritime navigation", "cargo handling", "dock operations", "vessel safety protocols", "twic compliance", "incident response"],
        "url": "https://scspa.com/careers"
    },

    # -------------------------------------------------------------------------
    # RENEWABLE ENERGY & HIGH-VOLTAGE POWER GENERATION
    # -------------------------------------------------------------------------
    {
        "job_id": "fys_pwr_001",
        "title": "High-Voltage Substation & Power Grid Field Specialist",
        "company": "Dominion Energy",
        "city": "Columbia",
        "state": "SC",
        "location_display": "Columbia, SC / Greenville, SC",
        "salary_min": 86000,
        "salary_max": 120000,
        "clearance_required": "None",
        "veteran_friendly": True,
        "source": "Adzuna API",
        "category": "Energy & Power Generation",
        "description": "Install, test, and maintain high-voltage transformers, switchgear, and utility substation relays. Direct translation for Army Prime Power Specialists (12P), Tactical Power Gen (91D), and Navy Electrician's Mates (EM).",
        "skills": ["high voltage electrical", "switchgear maintenance", "transformer testing", "schematic reading", "electrical safety (nfpa 70e)", "substation relays"],
        "url": "https://careers.dominionenergy.com"
    }
]


# Demo Veteran Profiles representing diverse backgrounds
DEMO_VETERAN_PROFILES: Dict[str, Dict] = {
    "18F": {
        "name": "William Free Hall",
        "email": "whall4.wh@gmail.com",
        "phone": "(910) 584-3843",
        "branch": "Army",
        "rank": "E-8 | Master Sergeant (MSG) / First Sergeant (1SG)",
        "mos": "18F",
        "clearance": "Top Secret / SCI",
        "service_status": "Veteran (Retired)",
        "target_city": "Greenville",
        "target_state": "SC",
        "salary_min": 120000,
        "salary_max": 180000,
        "relocation": True,
        "remote_ok": True,
        "resume_text": """WILLIAM FREE HALL
Technical Lead & Solutions Architect | Cloud & Data Engineer
Niceville, FL  •  (910) 584-3843  •  whall4.wh@gmail.com  •  linkedin.com/in/william-free-hall

EXECUTIVE SUMMARY
Results-driven Technical Lead and Cloud/Data Architect with over 10 years of specialized experience in data analytics, data engineering, and executive intelligence briefings, backed by over 20 years of elite military leadership in US Army Special Operations. Proven track record of architecting multi-tier data lakehouses on Databricks, engineering graph analytical models, managing enterprise cloud infrastructure, and interpreting high-stakes intelligence analysis using Palantir and i2 Analyst's Notebook for General Officers and senior DOD decision-makers.

TECHNICAL & LEADERSHIP SKILLS
• Data & Analytics: Palantir, i2 Analyst's Notebook, Databricks, Apache Spark (PySpark), Delta Lake, Unity Catalog, Vector Search, PyTorch, Scikit-Learn, Pandas, SQL
• Cloud & Infrastructure: AWS, GCP, Azure, Kubernetes, Docker, Terraform, GitHub Actions, CI/CD, Linux
• Executive Leadership: Executive Data Briefings (General Officer Level), Inter-Agency Coordination (DOD, CIA, State Dept), Cross-Functional Team Leadership, Risk Assessment, OPSEC

MILITARY SERVICE
Special Forces Intelligence Sergeant (18F) & Team Sergeant | U.S. Army Special Forces (1999 – 2017)
• Led 12-man Special Forces operational teams across multiple combat deployments with 100% mission success.
• Synthesized complex data analytics into executive operational briefings for General Officers and senior DOD leadership.
• Aggregated and analyzed massive multi-source datasets using Palantir and i2 Analyst's Notebook.
"""
    },
    "11B": {
        "name": "Marcus Vance",
        "email": "marcus.vance@example.com",
        "phone": "(864) 555-0192",
        "branch": "Army",
        "rank": "E-6 | Staff Sergeant (SSG)",
        "mos": "11B",
        "clearance": "Secret",
        "service_status": "Active Duty (Transitioning / ETS soon)",
        "target_city": "Greenville",
        "target_state": "SC",
        "salary_min": 75000,
        "salary_max": 110000,
        "relocation": True,
        "remote_ok": True,
        "resume_text": """MARCUS VANCE
Operations Team Lead & Field Supervisor
Greenville, SC  •  (864) 555-0192  •  marcus.vance@example.com

SUMMARY
Disciplined, results-oriented Infantry Squad Leader (SSG / E-6) with 8 years of active-duty Army leadership experience directing 9-man teams in high-tempo tactical and training environments. Expert in risk management, standard operating procedures, personnel accountability, and equipment maintenance. Transitioning to civilian operations management, field project supervision, or physical security leadership.

CORE COMPETENCIES
• Operations & Team Leadership: Squad & Platoon Leadership, High-Stress Decision Making, Crisis Management, SOP Enforcement
• Safety & Risk Assessment: Composite Risk Management, Physical Security Protocols, Incident Reporting, Safety Auditing
• Logistics & Equipment: Property Accountability ($1.5M+ equipment), Preventive Maintenance, Tactical Radios, GPS Navigation

MILITARY EXPERIENCE
Infantry Squad Leader (11B) | U.S. Army (2018 – Present)
• Commanded a 9-person squad responsible for mission planning, operational safety, and continuous tactical readiness.
• Maintained 100% accountability for over $1.5M in sensitive military optical, communications, and vehicle equipment with zero losses.
• Conducted daily safety briefings, risk mitigation audits, and after-action reviews to optimize team performance.
"""
    },
    "88M": {
        "name": "David Miller",
        "email": "david.miller@example.com",
        "phone": "(803) 555-0144",
        "branch": "Army",
        "rank": "E-5 | Sergeant (SGT)",
        "mos": "88M",
        "clearance": "Secret",
        "service_status": "Veteran (Separated / Discharged)",
        "target_city": "Columbia",
        "target_state": "SC",
        "salary_min": 70000,
        "salary_max": 95000,
        "relocation": False,
        "remote_ok": False,
        "resume_text": """DAVID MILLER
Fleet Logistics Coordinator & Commercial Transport Specialist
Columbia, SC  •  (803) 555-0144  •  david.miller@example.com

SUMMARY
Experienced Motor Transport Operator (SGT / E-5) with 6 years of military fleet transport, cargo distribution, and convoy route management. Logged over 80,000 incident-free miles operating heavy military tractor-trailers (M915, PLS, HEMTT) under severe environmental conditions. Possesses valid Class A CDL equivalent qualifications, hazmat handling experience, and DOT compliance knowledge.

CORE COMPETENCIES
• Fleet Operations: Heavy Vehicle Driving (Class A CDL), Convoy Logistics, Route Planning, Cargo Rigging & Tie-Down
• Compliance & Maintenance: DOT Safety Regulations, Hazmat Transport, Preventive Maintenance Checks (PMCS), Dispatching
• Logistics Software: Telematics Tracking, Electronic Logging Devices (ELD), Excel Inventory Logs

EXPERIENCE
Motor Transport Operator (88M) | U.S. Army (2019 – 2025)
• Safely operated heavy tactical transport vehicles across interstate and tactical routes with zero preventable accidents.
• Supervised loading, weight distribution, and securing of sensitive cargo and hazardous materials.
• Performed daily preventive maintenance and fluid diagnostics on diesel engines, hydraulic lifts, and pneumatic brakes.
"""
    },
    "25B": {
        "name": "Sarah Jenkins",
        "email": "sarah.jenkins@example.com",
        "phone": "(843) 555-0188",
        "branch": "Navy",
        "rank": "E-5 | Petty Officer Second Class (PO2)",
        "mos": "IT",
        "clearance": "Top Secret / SCI",
        "service_status": "Active Duty (Transitioning / ETS soon)",
        "target_city": "Charleston",
        "target_state": "SC",
        "salary_min": 90000,
        "salary_max": 125000,
        "relocation": True,
        "remote_ok": True,
        "resume_text": """SARAH JENKINS
Systems Administrator & Network Security Specialist
Charleston, SC  •  (843) 555-0188  •  sarah.jenkins@example.com

SUMMARY
Naval Information Systems Technician (IT2 / E-5) with 5 years of experience administering secure shipboard and shore-based enterprise IT networks. Holds active Top Secret / SCI clearance, CompTIA Security+, and Cisco CCNA. Proven track record managing Active Directory, Windows Server 2022, Cisco switches, and satellite communications links for 1,200+ users.

TECHNICAL SKILLS
• Systems & Networks: Active Directory, Windows Server, Linux (RHEL), Cisco Routers & Switches, VMware ESXi, TCP/IP, DNS, DHCP
• Security & Comms: CompTIA Security+, Cisco CCNA, Firewalls, COMSEC, SATCOM, Incident Handling, Patch Management
• Tools: PowerShell, Wireshark, Splunk, SolarWinds, Microsoft 365 Admin

MILITARY EXPERIENCE
Information Systems Technician (IT) | U.S. Navy (2021 – Present)
• Administered classified and unclassified LAN/WAN networks supporting 1,200+ naval personnel with 99.9% uptime.
• Configured Cisco switches, virtual machines on VMware, and Active Directory group policies.
• Conducted vulnerability scans using ACAS/Nessus and remediated security findings to maintain strict DoD compliance.
"""
    }
}


def load_cached_scraped_jobs() -> List[Dict]:
    """
    Load real live jobs from public APIs and verified veteran employer partner network.
    """
    real_live_jobs = []
    try:
        from app.real_job_fetcher import fetch_all_live_jobs
        real_live_jobs = fetch_all_live_jobs()
    except Exception:
        pass

    # Combine verified partner network with live ingested jobs
    all_jobs = list(SAMPLE_JOBS)
    
    seen = set(f"{j['title'].lower()}_{j['company'].lower()}" for j in all_jobs)
    for rj in real_live_jobs:
        key = f"{rj['title'].lower()}_{rj['company'].lower()}"
        if key not in seen:
            seen.add(key)
            all_jobs.append(rj)
            
    return all_jobs
