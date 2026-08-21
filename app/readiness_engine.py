"""
Career Readiness & Skill Gap Improvement Engine
For Your Service - 7 Eagle Group
Analyzes candidate embeddings, identifies missing high-impact certifications & skills,
calculates potential match score uplift and salary growth, and provides 100% free veteran funding links.
"""

from typing import Dict, List, Tuple

CAREER_TRACKS: Dict[str, Dict] = {
    "Cloud & DevOps Engineering": {
        "icon": "☁️",
        "core_skills": ["aws", "azure", "kubernetes", "docker", "terraform", "python", "linux", "ci/cd", "git"],
        "recommended_certs": [
            {
                "name": "AWS Certified Solutions Architect - Associate",
                "score_uplift": 18,
                "salary_uplift": 22000,
                "provider": "Amazon Web Services",
                "free_for_veterans": "AWS SkillBuilder & Onward to Opportunity (O2O) provide free training + exam vouchers.",
                "url": "https://aws.amazon.com/training/veterans/"
            },
            {
                "name": "Certified Kubernetes Administrator (CKA)",
                "score_uplift": 15,
                "salary_uplift": 18000,
                "provider": "Linux Foundation",
                "free_for_veterans": "Eligible for DoD COOL and GI Bill reimbursement.",
                "url": "https://www.cncf.io/certification/cka/"
            },
            {
                "name": "CompTIA Security+",
                "score_uplift": 12,
                "salary_uplift": 12000,
                "provider": "CompTIA",
                "free_for_veterans": "100% free via Onward to Opportunity (Syracuse IVMF).",
                "url": "https://ivmf.syracuse.edu/programs/career-training/"
            }
        ],
        "resume_tips": [
            ("Replace 'Comms NCOIC'", "Write 'Cloud & Network Infrastructure Lead'"),
            ("Replace 'Maintained tactical comms'", "Write 'Architected high-availability distributed network systems'")
        ]
    },
    "Cybersecurity & Information Assurance": {
        "icon": "🛡️",
        "core_skills": ["cybersecurity", "siem", "splunk", "wireshark", "penetration testing", "firewalls", "incident response", "security+", "cissp"],
        "recommended_certs": [
            {
                "name": "CompTIA Security+ (DoD 8570 Baseline)",
                "score_uplift": 22,
                "salary_uplift": 18000,
                "provider": "CompTIA",
                "free_for_veterans": "Free through Syracuse University IVMF (Onward to Opportunity) or VetSec.",
                "url": "https://ivmf.syracuse.edu/programs/career-training/"
            },
            {
                "name": "Certified Information Systems Security Professional (CISSP)",
                "score_uplift": 25,
                "salary_uplift": 32000,
                "provider": "(ISC)²",
                "free_for_veterans": "Funded through Army/Navy/Air Force COOL and DoD SkillBridge.",
                "url": "https://www.isc2.org/certifications/cissp"
            },
            {
                "name": "Certified Ethical Hacker (CEH)",
                "score_uplift": 15,
                "salary_uplift": 15000,
                "provider": "EC-Council",
                "free_for_veterans": "Supported by VA Veteran Readiness & Employment (VR&E).",
                "url": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/"
            }
        ],
        "resume_tips": [
            ("Replace 'COMSEC Custodian'", "Write 'Information Assurance & Cryptographic Key Management Lead'"),
            ("Replace 'Handled physical security & guards'", "Write 'Enforced DoD 8570 access control & perimeter defense protocols'")
        ]
    },
    "Operations, Program & Project Management": {
        "icon": "⚙️",
        "core_skills": ["operations management", "strategic planning", "risk management", "team leadership", "budget reconciliation", "process optimization", "standard operating procedures"],
        "recommended_certs": [
            {
                "name": "Project Management Professional (PMP)",
                "score_uplift": 20,
                "salary_uplift": 25000,
                "provider": "PMI",
                "free_for_veterans": "Free prep & exam funding through Onward to Opportunity (O2O).",
                "url": "https://ivmf.syracuse.edu/programs/career-training/"
            },
            {
                "name": "Lean Six Sigma Green Belt (LSSGB)",
                "score_uplift": 14,
                "salary_uplift": 14000,
                "provider": "IASSC / ASQ",
                "free_for_veterans": "Funded via Army Credentialing Assistance (CA) and Military COOL.",
                "url": "https://www.armyignited.army.mil/"
            },
            {
                "name": "Certified ScrumMaster (CSM)",
                "score_uplift": 12,
                "salary_uplift": 12000,
                "provider": "Scrum Alliance",
                "free_for_veterans": "Available via free veteran cohorts at VetsInTech.",
                "url": "https://vetsintech.co/"
            }
        ],
        "resume_tips": [
            ("Replace 'Platoon Sergeant / Squad Leader'", "Write 'Operations Supervisor directing cross-functional team of 10-40 personnel'"),
            ("Replace 'Responsible for mission execution'", "Write 'Delivered complex operational projects with 100% on-time milestone completion'")
        ]
    },
    "Logistics, Supply Chain & Fleet Management": {
        "icon": "🚚",
        "core_skills": ["supply chain", "inventory management", "logistics", "procurement", "fleet tracking", "dot compliance", "sap", "warehouse management", "cdl"],
        "recommended_certs": [
            {
                "name": "Commercial Driver's License (Class A CDL)",
                "score_uplift": 24,
                "salary_uplift": 20000,
                "provider": "State DMV / Military CDL Skills Waiver",
                "free_for_veterans": "Most states offer the Military CDL Skills Test Waiver Program for 88M, 3531, 2T2X1.",
                "url": "https://www.fmcsa.dot.gov/registration/commercial-drivers-license/military-skills-test-waiver-program"
            },
            {
                "name": "Certified in Production and Inventory Management (CPIM)",
                "score_uplift": 16,
                "salary_uplift": 16000,
                "provider": "ASCM / APICS",
                "free_for_veterans": "Funded via DoD Credentialing Assistance programs.",
                "url": "https://www.ascm.org/learning-development/certifications-credentials/cpim/"
            },
            {
                "name": "OSHA 30-Hour General Industry Certification",
                "score_uplift": 10,
                "salary_uplift": 8000,
                "provider": "OSHA",
                "free_for_veterans": "Available through local Veterans Transition Assistance Programs.",
                "url": "https://www.osha.gov/training/outreach/general-industry"
            }
        ],
        "resume_tips": [
            ("Replace 'Unit Supply Sergeant'", "Write 'Warehouse & Inventory Operations Manager ($2M+ asset portfolio)'"),
            ("Replace 'PMCS on vehicles'", "Write 'Conducted scheduled preventive maintenance & DOT compliance inspections'")
        ]
    },
    "Maintenance, Mechanics & Field Engineering": {
        "icon": "🔧",
        "core_skills": ["diesel mechanics", "hydraulics", "pneumatics", "electrical troubleshooting", "preventive maintenance", "diagnostic testing", "heavy equipment"],
        "recommended_certs": [
            {
                "name": "ASE Heavy Duty Truck Certification (T-Series)",
                "score_uplift": 22,
                "salary_uplift": 18000,
                "provider": "National Institute for Automotive Service Excellence",
                "free_for_veterans": "Funded through Army/Navy/Air Force COOL.",
                "url": "https://www.ase.com/"
            },
            {
                "name": "FAA Airframe and Powerplant (A&P) License",
                "score_uplift": 28,
                "salary_uplift": 28000,
                "provider": "Federal Aviation Administration (FAA)",
                "free_for_veterans": "Military Joint Service Aviation Maintenance Tech Certification Council (JSAMTCC) provides free voucher testing.",
                "url": "https://www.faa.gov/mechanics/become"
            },
            {
                "name": "EPA Universal Section 608 (HVAC/Refrigerant)",
                "score_uplift": 12,
                "salary_uplift": 10000,
                "provider": "EPA Approved Testing Organizations",
                "free_for_veterans": "Covered under GI Bill and military branch credentialing programs.",
                "url": "https://www.epa.gov/section608/section-608-technician-certification-programs"
            }
        ],
        "resume_tips": [
            ("Replace 'Motor Pool Mechanic'", "Write 'Heavy Fleet & Diesel Powertrain Specialist'"),
            ("Replace 'Repaired broken equipment in field'", "Write 'Executed rapid root-cause fault diagnosis & component-level overhaul'")
        ]
    },
    "Law Enforcement, Physical Security & Investigations": {
        "icon": "👮",
        "core_skills": ["force protection", "perimeter security", "access control", "cctv", "incident investigation", "conflict de-escalation", "emergency response", "risk assessment"],
        "recommended_certs": [
            {
                "name": "Physical Security Professional (PSP)",
                "score_uplift": 18,
                "salary_uplift": 15000,
                "provider": "ASIS International",
                "free_for_veterans": "Eligible for GI Bill and DoD Credentialing Assistance reimbursement.",
                "url": "https://www.asisonline.org/certification/physical-security-professional-psp/"
            },
            {
                "name": "Certified Protection Professional (CPP)",
                "score_uplift": 22,
                "salary_uplift": 22000,
                "provider": "ASIS International",
                "free_for_veterans": "Directly sponsored under DoD COOL for Senior NCOs and Officers.",
                "url": "https://www.asisonline.org/certification/certified-protection-professional-cpp/"
            },
            {
                "name": "Certified Fraud Examiner (CFE)",
                "score_uplift": 16,
                "salary_uplift": 16000,
                "provider": "ACFE",
                "free_for_veterans": "Funded through military law enforcement & CID credentialing.",
                "url": "https://www.acfe.com/"
            }
        ],
        "resume_tips": [
            ("Replace 'Guard duty / Access control point'", "Write 'Controlled entry point security & biometric verification for 5,000+ daily visitors'"),
            ("Replace 'MP Desk Sergeant'", "Write 'Emergency Dispatch & Incident Response Commander'")
        ]
    },
    "Healthcare, Emergency Medicine & Safety": {
        "icon": "🏥",
        "core_skills": ["emergency trauma care", "patient triage", "vital signs assessment", "medical documentation", "emr", "critical decision making", "cpr", "bls"],
        "recommended_certs": [
            {
                "name": "National Registry of Emergency Medical Technicians (NREMT-P)",
                "score_uplift": 25,
                "salary_uplift": 22000,
                "provider": "NREMT",
                "free_for_veterans": "Military Medic to Paramedic bridge programs funded through VA and State Veteran Commissions.",
                "url": "https://www.nremt.org/"
            },
            {
                "name": "Certified Healthcare Safety Professional (CHSP)",
                "score_uplift": 15,
                "salary_uplift": 14000,
                "provider": "IBFCSM",
                "free_for_veterans": "Supported through Army Credentialing Assistance.",
                "url": "https://ibfcsm.com/"
            }
        ],
        "resume_tips": [
            ("Replace 'Platoon Medic / Corpsman'", "Write 'Emergency Medical Operations Lead & Trauma Care Specialist'"),
            ("Replace 'Administered medical supplies'", "Write 'Managed clinical pharmaceutical inventory & patient medical documentation (EMR)'")
        ]
    }
}


def analyze_career_readiness(
    target_track_name: str,
    candidate_skills: List[str],
    current_match_score: float
) -> Dict:
    """
    Analyzes the candidate's skills against their selected career track.
    Computes missing skills, projected match score uplift, salary growth,
    and high-impact free certifications.
    """
    track = CAREER_TRACKS.get(target_track_name, CAREER_TRACKS["Operations, Program & Project Management"])

    user_skills_lower = [s.lower() for s in candidate_skills]
    core_skills = track["core_skills"]

    # Identify missing core skills
    missing_skills = [s for s in core_skills if s not in user_skills_lower]
    matching_skills = [s for s in core_skills if s in user_skills_lower]

    # Calculate potential uplift
    potential_score = min(98.0, current_match_score + 18.0)
    top_cert = track["recommended_certs"][0] if track["recommended_certs"] else None
    est_salary_uplift = sum([c["salary_uplift"] for c in track["recommended_certs"][:2]]) // 2 if track["recommended_certs"] else 15000

    return {
        "target_track": target_track_name,
        "icon": track["icon"],
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "current_score": current_match_score,
        "projected_score": round(potential_score, 1),
        "score_gain": round(potential_score - current_match_score, 1),
        "est_salary_uplift": est_salary_uplift,
        "recommended_certs": track["recommended_certs"],
        "resume_tips": track["resume_tips"]
    }
