# ============================================================================
# For Your Service - Veteran Intake & Job Matching Portal 🇺🇸
# Universal Platform for ALL Service Members: Any Branch, Any Rank, Any Clearance
# Powered by 7 Eagle Group | AI-Driven Veteran Placement Platform
# Developer: Free Hall (18Z / 18F, US Army Special Forces, Ret.)
# ============================================================================

import streamlit as st

# ============================================================================
# MUST BE FIRST STREAMLIT COMMAND
# ============================================================================
st.set_page_config(
    page_title="For Your Service — 7 Eagle Group",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import uuid
import json
import re
import io
import os
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import local modules with safe dual fallback for Databricks Apps root execution
try:
    from mos_data import MOS_DATABASE, BRANCH_RANKS, lookup_mos, get_mos_choices_by_branch
    from sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILES, load_cached_scraped_jobs
    from readiness_engine import CAREER_TRACKS, analyze_career_readiness
    from geo_database import CITY_COORDINATES, lookup_city_coordinates
    from pdf_generator import generate_veteran_transition_pdf
    from defense_contractor_fetcher import fetch_defense_contractor_jobs
    from linkedin_veteran_finder import LinkedInVeteranFinder, get_curated_ge_aerospace_targets
except ImportError:
    from app.mos_data import MOS_DATABASE, BRANCH_RANKS, lookup_mos, get_mos_choices_by_branch
    from app.sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILES, load_cached_scraped_jobs
    from app.readiness_engine import CAREER_TRACKS, analyze_career_readiness
    from app.geo_database import CITY_COORDINATES, lookup_city_coordinates
    from app.pdf_generator import generate_veteran_transition_pdf
    from app.defense_contractor_fetcher import fetch_defense_contractor_jobs
    from app.linkedin_veteran_finder import LinkedInVeteranFinder, get_curated_ge_aerospace_targets

# Check for Databricks / PySpark compute availability safely
SPARK_AVAILABLE = False
spark = None
if os.getenv("DATABRICKS_RUNTIME_VERSION") or os.getenv("DATABRICKS_SERVER_HOSTNAME"):
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        SPARK_AVAILABLE = True
    except Exception:
        spark = None
        SPARK_AVAILABLE = False

# ============================================================================
# LIVE VISITOR & USAGE METRICS TRACKER
# ============================================================================

METRICS_DIR = Path(__file__).resolve().parent.parent / "data" / "analytics"
METRICS_FILE = METRICS_DIR / "usage_metrics.json"
FALLBACK_METRICS_FILE = Path("/tmp/fys_usage_metrics.json")

def get_platform_metrics(increment_visit=False, increment_match=False, increment_intro=False) -> Dict[str, int]:
    """Retrieve and atomically update daily platform visitor and usage counters (resets daily to 0)"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    default_metrics = {
        "metric_date": today_str,
        "total_visitors": 0,
        "total_matches_run": 0,
        "veterans_connected": 0,
        "last_updated": datetime.now().isoformat()
    }

    target_file = METRICS_FILE
    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        target_file = FALLBACK_METRICS_FILE
        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    metrics = default_metrics.copy()
    if target_file.exists():
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
                saved_date = saved.get("metric_date") or saved.get("date")
                if saved_date == today_str:
                    metrics["total_visitors"] = int(saved.get("total_visitors", 0))
                    metrics["total_matches_run"] = int(saved.get("total_matches_run", 0))
                    metrics["veterans_connected"] = int(saved.get("veterans_connected", 0))
                else:
                    # New day: automatically reset counters to 0
                    metrics["total_visitors"] = 0
                    metrics["total_matches_run"] = 0
                    metrics["veterans_connected"] = 0
        except Exception:
            pass

    if increment_visit:
        metrics["total_visitors"] += 1
    if increment_match:
        metrics["total_matches_run"] += 1
    if increment_intro:
        metrics["veterans_connected"] += 1

    if increment_visit or increment_match or increment_intro or not target_file.exists():
        metrics["metric_date"] = today_str
        metrics["last_updated"] = datetime.now().isoformat()
        try:
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
        except Exception:
            try:
                with open(FALLBACK_METRICS_FILE, "w", encoding="utf-8") as f:
                    json.dump(metrics, f, indent=2)
            except Exception:
                pass

    return metrics

# Session Tracking: Increment visit count once per unique browser session
if "session_counted" not in st.session_state:
    st.session_state["session_counted"] = True
    platform_metrics = get_platform_metrics(increment_visit=True)
else:
    platform_metrics = get_platform_metrics()

# ============================================================================
# PATRIOTIC STYLING & RESPONSIVE THEME
# ============================================================================

# Custom Responsive Patriotic CSS (iOS, Android, Mac Safari, Chrome, Edge Compatible)
st.markdown("""
<style>
    /* Viewport & Cross-Platform Typography */
    html, body, [class*="css"] {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        -webkit-text-size-adjust: 100%;
        text-rendering: optimizeLegibility;
    }

    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* iOS Safari Input Zoom Fix */
    input, select, textarea, .stTextInput input, .stSelectbox select {
        font-size: 16px !important;
    }

    /* Responsive Hero Banner */
    .hero-banner {
        background: -webkit-linear-gradient(135deg, #0b1d3a 0%, #1e3a8a 50%, #13315c 100%);
        background: linear-gradient(135deg, #0b1d3a 0%, #1e3a8a 50%, #13315c 100%);
        color: white;
        padding: clamp(1rem, 3vw, 2rem) clamp(1rem, 4vw, 2.5rem);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(11, 29, 58, 0.25);
        margin-bottom: 1.25rem;
        border-bottom: 5px solid #c81d25;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    .hero-title {
        font-size: clamp(1.4rem, 5vw, 2.3rem);
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: clamp(0.9rem, 2.5vw, 1.15rem);
        color: #e2e8f0;
        margin-top: 0.5rem;
        font-weight: 400;
        line-height: 1.35;
    }
    .hero-badge {
        display: inline-block;
        background: #d4af37;
        color: #0b1d3a;
        font-size: clamp(0.75rem, 2vw, 0.85rem);
        font-weight: 700;
        padding: 0.3rem 0.85rem;
        border-radius: 20px;
        margin-top: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Responsive Branch Grid */
    .branch-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 0.5rem;
        margin-bottom: 1.25rem;
    }
    .branch-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #1e3a8a;
        border-radius: 8px;
        padding: 0.75rem 0.4rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        font-size: 0.85rem;
    }

    /* Match Badges */
    .match-badge-high {
        background-color: #15803d;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }
    .match-badge-med {
        background-color: #d97706;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }

    /* Responsive Job Cards */
    .job-card {
        background: white;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3a8a;
        border-radius: 10px;
        padding: clamp(0.85rem, 2.5vw, 1.25rem);
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* Skill Chips */
    .skill-chip {
        display: inline-block;
        background: #e0e7ff;
        color: #1e3a8a;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        margin-right: 0.3rem;
        margin-bottom: 0.35rem;
        border: 1px solid #c7d2fe;
    }
    .mil-skill-chip {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        margin-right: 0.3rem;
        margin-bottom: 0.35rem;
        border: 1px solid #fde68a;
    }
    .ops-skill-chip {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        margin-right: 0.3rem;
        margin-bottom: 0.35rem;
        border: 1px solid #bbf7d0;
    }

    /* Clearance Badge */
    .clearance-badge {
        background: #0f172a;
        color: #f8fafc;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid #475569;
        display: inline-block;
    }

    /* Mobile & Touch Optimized Buttons */
    .stButton>button {
        background-color: #1e3a8a;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        min-height: 44px;
        touch-action: manipulation;
        -webkit-tap-highlight-color: transparent;
    }
    .stButton>button:hover, .stButton>button:active {
        background-color: #0b1d3a;
        color: #ffffff;
    }

    /* Media Queries for Mobile Screens (Phones < 768px) */
    @media (max-width: 768px) {
        .branch-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.4rem;
        }
        .branch-card {
            padding: 0.5rem 0.25rem;
            font-size: 0.8rem;
        }
        .hero-banner {
            padding: 1rem 0.85rem;
            border-radius: 8px;
        }
        .job-card {
            padding: 0.85rem 0.75rem;
        }
        .stButton>button {
            width: 100% !important;
            margin-bottom: 0.35rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS: RESUME PARSING & SKILL EXTRACTION
# ============================================================================

def extract_text_from_file(uploaded_file) -> str:
    """Extract raw text from uploaded PDF, DOCX, or TXT file (100% free & local)"""
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".pdf"):
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(uploaded_file)
                text = "".join([page.extract_text() or "" for page in reader.pages])
                return text
            except Exception:
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                text = "".join([page.extract_text() or "" for page in reader.pages])
                return text

        elif filename.endswith(".docx"):
            import docx
            doc = docx.Document(uploaded_file)
            return "\n".join([p.text for p in doc.paragraphs])

        elif filename.endswith(".txt"):
            return uploaded_file.getvalue().decode("utf-8", errors="ignore")

        else:
            return uploaded_file.getvalue().decode("utf-8", errors="ignore")

    except Exception as e:
        st.warning(f"⚠️ Note during file reading: {str(e)}. You can also paste resume text directly.")
        return ""


def parse_veteran_skills(resume_text: str, mos_code: str = "") -> Dict:
    """
    Extract technical skills, military leadership competencies, operations skills,
    and estimate years of service from resume text and MOS code.
    """
    text_lower = resume_text.lower()

    # 1. Technical & Software Skills Taxonomy
    tech_keywords = [
        "aws", "azure", "gcp", "kubernetes", "docker", "terraform", "python", "java",
        "javascript", "sql", "bash", "powershell", "jenkins", "github", "gitlab",
        "ci/cd", "devops", "linux", "windows", "windows server", "ansible", "cisco",
        "active directory", "palantir", "databricks", "spark", "pyspark", "delta lake",
        "networking", "cybersecurity", "siem", "splunk", "wireshark", "penetration testing",
        "security+", "cissp", "vmware", "tableau", "power bi", "excel", "satcom", "cryptography"
    ]

    # 2. Trades, Mechanics & Industrial Engineering Skills
    trades_keywords = [
        "diesel mechanics", "diesel engine", "hydraulics", "pneumatics", "welding",
        "fabrication", "engine overhaul", "electrical troubleshooting", "blueprint reading",
        "cnc machining", "machining", "lathe", "mill", "hvac", "plumbing", "carpentry",
        "rigging", "crane operation", "preventive maintenance", "diagnostic testing",
        "heavy equipment", "a&p license", "aviation maintenance", "turbine engine",
        "rotor systems", "precision torque", "switchgear", "substation", "transformer"
    ]

    # 3. Logistics, Supply Chain & Transportation Skills
    logistics_keywords = [
        "supply chain", "inventory management", "logistics", "procurement", "property accountability",
        "cdl", "class a cdl", "dot compliance", "telematics", "warehouse management",
        "shipping & receiving", "freight dispatch", "convoy operations", "forklift",
        "material handling", "sap", "erp", "fleet tracking", "asset tracking", "cargo rigging"
    ]

    # 4. Construction & Infrastructure Skills
    construction_keywords = [
        "earthmoving", "excavating", "surveying", "asphalt", "concrete", "framing",
        "osha 30", "osha compliance", "site supervision", "subcontractor management",
        "project scheduling", "blueprint interpretation", "heavy civil", "demolition"
    ]

    # 5. Law Enforcement, Security & Protection Skills
    security_keywords = [
        "force protection", "perimeter security", "access control", "cctv", "physical security",
        "felony investigations", "incident investigation", "conflict de-escalation",
        "emergency response", "evidence handling", "debriefing", "interpersonal interviewing",
        "case file preparation", "background checks", "security audits"
    ]

    # 6. Healthcare, Emergency Medicine & Safety
    healthcare_keywords = [
        "emergency trauma care", "patient triage", "vital signs assessment", "medical documentation",
        "emr", "critical decision making", "cpr", "bls", "acls", "paramedic", "patient care",
        "wound care", "field sanitation", "medevac", "pharmacology", "hazmat compliance"
    ]

    # 7. Military Leadership & Command Competencies
    leadership_keywords = [
        "executive briefings", "cross-functional leadership", "mission planning",
        "risk management", "opsec", "link analysis", "operations management",
        "crisis decision making", "inter-agency coordination", "team sergeant",
        "squad leader", "platoon sergeant", "command", "process optimization",
        "standard operating procedures", "personnel accountability", "after-action reviews",
        "situational awareness", "mentorship", "inspections", "training & development"
    ]

    def has_keyword(kw: str) -> bool:
        # Exact word-boundary match to prevent false positives (e.g. 'security' matching 'security+')
        pattern = r'(?:\b|_)' + re.escape(kw) + r'(?:\b|_)'
        return bool(re.search(pattern, text_lower))

    detected_tech = [s for s in tech_keywords if has_keyword(s)]
    detected_trades = [s for s in trades_keywords if has_keyword(s)]
    detected_logistics = [s for s in logistics_keywords if has_keyword(s)]
    detected_construction = [s for s in construction_keywords if has_keyword(s)]
    detected_security = [s for s in security_keywords if has_keyword(s)]
    detected_healthcare = [s for s in healthcare_keywords if has_keyword(s)]
    detected_leadership = [s for s in leadership_keywords if has_keyword(s)]

    detected_ops = list(set(detected_trades + detected_logistics + detected_construction + detected_security + detected_healthcare))

    # MOS information is kept separate as background context, NEVER injected as claimed personal skills/certs
    mos_info = lookup_mos(mos_code)
    mos_skills = mos_info.get("transferable_skills", []) if mos_info else []

    # Estimate years of experience from resume text
    years_pattern = r'(\d+)\+?\s*years?'
    years_matches = re.findall(years_pattern, text_lower)
    total_years = max([int(y) for y in years_matches], default=4)

    if total_years >= 12:
        seniority = "Senior / Executive Leader"
    elif total_years >= 6:
        seniority = "Mid-to-Senior Professional"
    else:
        seniority = "Associate / Specialist"

    return {
        "technical_skills": list(set(detected_tech)),
        "leadership_skills": list(set(detected_leadership)),
        "ops_skills": list(set(detected_ops)),
        "mos_skills": mos_skills,
        "total_years": total_years,
        "seniority": seniority
    }


# ============================================================================
# GEOGRAPHIC DISTANCE & COMMUTE RADIUS ENGINE
# ============================================================================


def haversine_distance_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in miles between two latitude/longitude coordinates."""
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


def get_city_coordinates(city: str, state: str) -> Optional[Tuple[float, float]]:
    """Lookup coordinates for any city and state across all 50 states."""
    return lookup_city_coordinates(city, state)


def estimate_job_distance(
    candidate_city: str,
    candidate_state: str,
    job_city: str,
    job_state: str,
    job_location_display: str
) -> Optional[float]:
    """Estimate distance in miles between candidate target city and job location."""
    loc_lower = f"{job_city} {job_state} {job_location_display}".lower()
    if "remote" in loc_lower or "anywhere" in loc_lower or "virtual" in loc_lower:
        return 0.0

    c_coords = get_city_coordinates(candidate_city, candidate_state)
    j_coords = get_city_coordinates(job_city, job_state)

    if c_coords and j_coords:
        return haversine_distance_miles(c_coords[0], c_coords[1], j_coords[0], j_coords[1])

    # Same city/metro
    if candidate_city.lower().strip() == job_city.lower().strip() and candidate_state.lower().strip() == job_state.lower().strip():
        return 5.0

    # Same state
    if candidate_state.lower().strip() == job_state.lower().strip():
        return 45.0

    return 500.0


# ============================================================================
# CLEARANCE HIERARCHY & EVALUATION ENGINE
# ============================================================================

CLEARANCE_RANKS = {
    "none": 0,
    "none / public trust": 1,
    "public trust": 1,
    "confidential": 2,
    "secret": 3,
    "active secret": 3,
    "top secret": 4,
    "active top secret": 4,
    "top secret / sci": 5,
    "ts / sci": 5,
    "ts/sci": 5,
    "ts / sci with ci poly": 6,
    "ts / sci with full scope poly": 7,
    "poly": 6
}


def get_clearance_rank(clr_str: str) -> int:
    """Extract normalized numeric rank (0-7) for a security clearance string."""
    if not clr_str:
        return 0
    c = str(clr_str).lower().strip()
    for k, v in CLEARANCE_RANKS.items():
        if k == c:
            return v
    if "full scope" in c or "fsp" in c:
        return 7
    if "ci poly" in c or "poly" in c:
        return 6
    if "sci" in c or "ts/sci" in c:
        return 5
    if "top secret" in c or "ts" in c:
        return 4
    if "secret" in c:
        return 3
    if "confidential" in c:
        return 2
    if "public trust" in c:
        return 1
    return 0


def evaluate_clearance(candidate_clearance: str, job_requirement: str) -> Tuple[bool, int, str, str]:
    """
    Accurately evaluate candidate's active clearance against job requirement.
    Returns: (is_eligible, points, status, detail_text)
    """
    cand_rank = get_clearance_rank(candidate_clearance)
    job_rank = get_clearance_rank(job_requirement)

    if job_rank == 0:
        # Job requires NO clearance (Direct civilian entry)
        return True, 15, "pass", "No clearance required (Direct civilian entry)"
    elif cand_rank >= job_rank:
        # Candidate clearance satisfies or exceeds requirement
        return True, 20, "pass", f"Active {candidate_clearance} satisfies requirement ({job_requirement})"
    else:
        # Candidate does not hold the required clearance
        return False, -40, "fail", f"Requires active {job_requirement} (You indicated: {candidate_clearance})"


# ============================================================================
# CAREER TRACK DOMAIN RULES & CROSS-DOMAIN GUARDRAILS
# ============================================================================

TRACK_DOMAIN_RULES = {
    "Cloud & DevOps Engineering": {
        "allowed_categories": [
            "Information Technology & Cloud",
            "Information Technology",
            "Cloud & DevOps",
            "Software Engineering",
            "Cybersecurity & Intelligence",
            "Intelligence & Analytics",
            "Data Engineering",
            "Systems Engineering"
        ],
        "primary_keywords": ["cloud", "devops", "software", "engineer", "data", "developer", "aws", "azure", "gcp", "python", "kubernetes", "terraform", "platform", "backend", "full-stack", "sysadmin", "infrastructure engineer", "solutions architect", "architect", "technology", "it", "sre", "database", "analytics"],
        "disallowed_categories": [
            "Logistics & Supply Chain",
            "Logistics & Transportation",
            "Maintenance & Mechanics",
            "Aviation & Maintenance",
            "Law Enforcement & Security",
            "Healthcare & Medical",
            "Construction & Infrastructure",
            "Advanced Manufacturing & Machining",
            "Maritime & Port Operations"
        ]
    },
    "Cybersecurity & Intelligence": {
        "allowed_categories": [
            "Cybersecurity & Intelligence",
            "Intelligence & Analytics",
            "Information Technology & Cloud",
            "Information Technology",
            "Security & Intelligence"
        ],
        "primary_keywords": ["cyber", "security", "threat", "soc", "infosec", "penetration", "vulnerability", "incident response", "intelligence", "analyst", "clearance", "cryptography"],
        "disallowed_categories": [
            "Logistics & Supply Chain",
            "Logistics & Transportation",
            "Maintenance & Mechanics",
            "Healthcare & Medical",
            "Construction & Infrastructure"
        ]
    },
    "Logistics, Supply Chain & Fleet Transportation": {
        "allowed_categories": [
            "Logistics & Supply Chain",
            "Logistics & Transportation",
            "Maritime & Port Operations",
            "Transportation & Logistics",
            "Warehouse Operations"
        ],
        "primary_keywords": ["logistics", "supply chain", "freight", "transportation", "warehouse", "dispatcher", "fleet", "cdl", "distribution", "inventory", "shipping", "property"],
        "disallowed_categories": [
            "Information Technology & Cloud",
            "Information Technology",
            "Software Engineering",
            "Healthcare & Medical"
        ]
    },
    "Operations, Program & Project Management": {
        "allowed_categories": [
            "Operations & Leadership",
            "General Operations",
            "Program Management",
            "Project Management",
            "Field Operations"
        ],
        "primary_keywords": ["operations", "project manager", "program manager", "coordinator", "director", "supervisor", "superintendent", "continuous improvement", "pmp", "operational leadership"],
        "disallowed_categories": [
            "Healthcare & Medical"
        ]
    },
    "Maintenance, Aviation & Precision Manufacturing": {
        "allowed_categories": [
            "Maintenance & Mechanics",
            "Aviation & Maintenance",
            "Advanced Manufacturing & Machining",
            "Energy & Power Generation",
            "Precision Machining"
        ],
        "primary_keywords": ["maintenance", "mechanic", "aviation", "diesel", "technician", "hvac", "machinist", "manufacturing", "cnc", "turbines", "electrical maintenance"],
        "disallowed_categories": [
            "Information Technology & Cloud",
            "Healthcare & Medical"
        ]
    },
    "Law Enforcement, Physical Security & Investigations": {
        "allowed_categories": [
            "Law Enforcement & Security",
            "Physical Security",
            "Corporate Investigations"
        ],
        "primary_keywords": ["law enforcement", "police", "investigator", "physical security", "patrol", "compliance", "guard", "protection officer", "asset protection"],
        "disallowed_categories": [
            "Healthcare & Medical",
            "Information Technology & Cloud"
        ]
    },
    "Healthcare, Emergency Services & Safety": {
        "allowed_categories": [
            "Healthcare & Medical",
            "Emergency Medical Services",
            "Environmental Health & Safety"
        ],
        "primary_keywords": ["nurse", "medical", "paramedic", "emt", "health", "clinical", "triage", "ehs", "patient", "safety officer"],
        "disallowed_categories": [
            "Logistics & Supply Chain",
            "Maintenance & Mechanics",
            "Information Technology & Cloud"
        ]
    },
    "Heavy Construction & Civil Infrastructure": {
        "allowed_categories": [
            "Construction & Infrastructure",
            "Civil Construction",
            "Heavy Infrastructure"
        ],
        "primary_keywords": ["construction", "civil", "superintendent", "estimator", "field engineer", "site supervisor", "heavy civil", "earthwork"],
        "disallowed_categories": [
            "Information Technology & Cloud",
            "Healthcare & Medical"
        ]
    }
}


def calculate_veteran_match_score(
    job: Dict,
    veteran_profile: Dict,
    extracted_skills: Dict
) -> Tuple[float, List[str], Dict]:
    """
    Calculate match score (0-100), 'Why You Match' reasons, and an individual
    Key Match Factors breakdown with self-improvement projected success metrics.
    Enforces hard track domain boundaries, accurate clearance hierarchy, and heavy technical stack weighting.
    """
    score = 0.0
    reasons = []

    job_title = job.get('title', '').lower().strip()
    job_desc = job.get('description', '').lower()
    job_category = job.get('category', '').strip()
    job_cat_lower = job_category.lower()
    job_text = f"{job_title} {job_desc} {job_cat_lower}"

    user_tech = set(extracted_skills.get("technical_skills", []))
    user_leadership = set(extracted_skills.get("leadership_skills", []))
    user_ops = set(extracted_skills.get("ops_skills", []))
    all_user_skills = user_tech.union(user_leadership).union(user_ops)

    target_track = veteran_profile.get("target_track", "").strip()
    desired_role_raw = veteran_profile.get("desired_role", "").lower().strip()

    # Parse multiple comma/slash/pipe separated desired titles
    desired_roles = [r.strip() for r in re.split(r'[,;/|]+', desired_role_raw) if len(r.strip()) >= 2]

    # -------------------------------------------------------------------------
    # 1. HARD TRACK BOUNDARY & REQUESTED ROLE PRIORITIZATION (Max 40 pts)
    # -------------------------------------------------------------------------
    title_matched_name = None
    role_priority = 5  # Default

    # Check if candidate explicitly requested a specific title
    if desired_roles:
        for dr in desired_roles:
            if dr in job_title or job_title in dr:
                title_matched_name = dr
                role_priority = 1
                break
            dr_words = [w for w in dr.split() if len(w) > 2 and w not in ["and", "the", "for", "with", "all"]]
            if dr_words and all(w in job_title for w in dr_words):
                title_matched_name = dr
                role_priority = 1
                break
            elif dr_words and any(w in job_title for w in dr_words):
                title_matched_name = dr
                role_priority = 2

        if role_priority > 2:
            for dr in desired_roles:
                if dr in job_cat_lower or dr in job_desc:
                    title_matched_name = dr
                    role_priority = 3
                    break

    # Check track domain rules (Prevent cross-domain bleed)
    track_rules = TRACK_DOMAIN_RULES.get(target_track, {})
    is_disallowed = False
    is_allowed = False

    if track_rules:
        disallowed_cats = track_rules.get("disallowed_categories", [])
        allowed_cats = track_rules.get("allowed_categories", [])

        if any(dc.lower() in job_cat_lower for dc in disallowed_cats):
            is_disallowed = True
        elif any(ac.lower() in job_cat_lower for ac in allowed_cats):
            is_allowed = True
        elif any(kw in job_title or kw in job_cat_lower for kw in track_rules.get("primary_keywords", [])):
            is_allowed = True
    else:
        is_allowed = True

    # If job is in a disallowed domain and user did NOT explicitly request this title -> Cross-domain block
    is_custom_match = False
    if is_disallowed and role_priority > 2:
        role_priority = 99  # Disallowed cross-domain job
        score -= 45
        role_status = "warn"
        role_detail = f"Cross-Domain (Outside {target_track})"
    elif role_priority == 1:
        is_custom_match = True
        score += 40
        role_status = "pass"
        role_detail = f"Exact match for requested title '{title_matched_name.title()}'"
        reasons.append(f"🎯 Requested Job Title: Exact match for '{title_matched_name.title()}'")
    elif role_priority == 2:
        is_custom_match = True
        score += 32
        role_status = "pass"
        role_detail = f"Keyword match for requested role '{title_matched_name.title()}'"
        reasons.append(f"🎯 Requested Role Alignment: Matches keywords for '{title_matched_name.title()}'")
    elif role_priority == 3:
        is_custom_match = True
        score += 24
        role_status = "pass"
        role_detail = f"Aligned with requested specialty '{title_matched_name.title()}'"
        reasons.append(f"🎯 Requested Role Focus: Context match for '{title_matched_name.title()}'")
    elif is_allowed:
        role_priority = 4 if desired_roles else 1
        score += 20 if desired_roles else 35
        role_status = "pass"
        role_detail = f"Direct match for {target_track}"
        reasons.append(f"🎯 Target Career Track: Aligns with your selected industry track ({target_track})")
    else:
        role_priority = 6 if desired_roles else 5
        score -= 30
        role_status = "warn"
        role_detail = f"Secondary Field (Outside {target_track})"

    # -------------------------------------------------------------------------
    # 2. TECHNICAL & CORE SKILLS OVERLAP (Max 40 pts)
    # -------------------------------------------------------------------------
    job_req_skills = [s.lower() for s in job.get("skills", [])]
    is_tech_track = target_track in ["Cloud & DevOps Engineering", "Cybersecurity & Intelligence"]
    is_tech_job = any(w in job_cat_lower or w in job_title for w in ["information technology", "cloud", "software", "cyber", "data", "devops", "platform", "systems engineer"])

    matched_skills = []
    missing_skills = []

    if job_req_skills:
        matched_skills = [s for s in job_req_skills if s in all_user_skills]
        missing_skills = [s for s in job_req_skills if s not in all_user_skills]
        skill_pct = len(matched_skills) / max(1, len(job_req_skills))

        # In tech tracks, technical overlap is weighted heavily (40 pts)
        score += skill_pct * 40.0

        if matched_skills:
            reasons.append(f"Skill Alignment: Verified match on {', '.join([s.title() for s in matched_skills[:4]])}")
        else:
            if is_tech_job and len(user_tech) == 0:
                score -= 25.0

        skills_status = "pass" if skill_pct >= 0.4 else "warn"
        skills_detail = f"{len(matched_skills)} of {len(job_req_skills)} Core Competencies Matched"
    else:
        # Evaluate user technical skills in job text
        tech_in_text = [s for s in user_tech if s in job_text]
        matched_skills = tech_in_text if is_tech_track else [s for s in all_user_skills if s in job_text]
        missing_skills = []

        if is_tech_track and tech_in_text:
            score += min(40.0, len(tech_in_text) * 8.0)
            reasons.append(f"Technical Stack Alignment: Verified match on {', '.join([s.upper() for s in tech_in_text[:4]])}")
            skills_status = "pass"
            skills_detail = f"{len(tech_in_text)} Core Tech Stack Tools Verified"
        elif is_tech_job and len(user_tech) == 0:
            score -= 25.0
            skills_status = "warn"
            skills_detail = "0 Technical Skills Detected"
        else:
            score += min(25.0, len(matched_skills) * 5.0)
            skills_status = "pass" if matched_skills else "warn"
            skills_detail = f"{len(matched_skills)} Relevant Strengths Identified"
            if matched_skills:
                reasons.append(f"Key Strengths: {', '.join([s.title() for s in matched_skills[:4]])}")

    # -------------------------------------------------------------------------
    # 3. SECURITY CLEARANCE EVALUATION (Max 20 pts or -40 pts penalty)
    # -------------------------------------------------------------------------
    job_clearance = str(job.get("clearance_required", "None")).strip()
    vet_clearance = str(veteran_profile.get("clearance", "None")).strip()

    clr_eligible, clr_pts, clr_status, clr_detail = evaluate_clearance(vet_clearance, job_clearance)
    score += clr_pts
    if clr_eligible:
        if job_clearance not in ["None", "None / Public Trust", ""]:
            reasons.append(f"🛡️ Security Clearance: Active {vet_clearance} qualifies for defense requirement ({job_clearance})")
        else:
            reasons.append("🛡️ Security Clearance: No clearance required (Direct civilian entry)")
    else:
        reasons.append(f"⛔ Clearance Ineligible: Requires active {job_clearance} (You indicated: {vet_clearance})")

    # -------------------------------------------------------------------------
    # 4. SALARY ALIGNMENT (Max 10 pts)
    # -------------------------------------------------------------------------
    job_sal_min = float(job.get("salary_min", 0) or 0)
    job_sal_max = float(job.get("salary_max", 0) or 0)
    vet_sal_min = float(veteran_profile.get("salary_min", 0) or 0)
    vet_sal_max = float(veteran_profile.get("salary_max", 0) or 0)

    if job_sal_max >= vet_sal_min and job_sal_min <= vet_sal_max:
        score += 10
        salary_status = "pass"
        salary_detail = f"${job_sal_min:,.0f} - ${job_sal_max:,.0f} (Within target ${vet_sal_min:,.0f} - ${vet_sal_max:,.0f})"
        reasons.append("Compensation: Perfectly aligns with your target salary")
    elif job_sal_max >= vet_sal_min * 0.85:
        score += 6
        salary_status = "warn"
        salary_detail = f"${job_sal_min:,.0f} - ${job_sal_max:,.0f} (Near target ${vet_sal_min:,.0f})"
    else:
        score += 2
        salary_status = "warn"
        salary_detail = f"${job_sal_min:,.0f} - ${job_sal_max:,.0f}"

    # -------------------------------------------------------------------------
    # 5. LOCATION, COMMUTE & TRAVEL RADIUS (Max 10 pts)
    # -------------------------------------------------------------------------
    vet_city = veteran_profile.get("target_city", "").strip()
    vet_state = veteran_profile.get("target_state", "").strip().upper()
    max_radius_str = str(veteran_profile.get("target_radius", "50 miles")).lower()
    remote_ok = veteran_profile.get("remote_ok", True)
    if "relocate" in veteran_profile:
        relocate_ok = bool(veteran_profile.get("relocate"))
    elif "relocation" in veteran_profile:
        relocate_ok = bool(veteran_profile.get("relocation"))
    else:
        relocate_ok = False

    if "10" in max_radius_str and "100" not in max_radius_str:
        max_radius = 10.0
    elif "20" in max_radius_str and "200" not in max_radius_str:
        max_radius = 20.0
    elif "25" in max_radius_str:
        max_radius = 25.0
    elif "50" in max_radius_str:
        max_radius = 50.0
    elif "100" in max_radius_str:
        max_radius = 100.0
    elif "200" in max_radius_str:
        max_radius = 200.0
    elif "any" in max_radius_str or "nationwide" in max_radius_str:
        max_radius = 9999.0
    else:
        max_radius = 50.0

    job_city = job.get("city", "").strip()
    job_state = job.get("state", "").strip().upper()
    job_loc_display = job.get("location_display", "")

    dist = estimate_job_distance(vet_city, vet_state, job_city, job_state, job_loc_display) if (vet_city and vet_state) else None
    is_remote_job = "remote" in job_loc_display.lower() or "remote" in job_city.lower() or "anywhere" in job_loc_display.lower()

    if is_remote_job:
        score += 10
        loc_status = "pass"
        loc_detail = "Remote / Flexible location"
        reasons.append("📍 Location: Remote / Flexible work mode")
    elif dist is not None and dist <= max_radius:
        score += 10
        loc_status = "pass"
        loc_detail = f"Local ({dist:.0f} mi from {vet_city.title()}, {vet_state} — within {int(max_radius)} mi radius)"
        reasons.append(f"📍 Commute Radius: {dist:.0f} miles from {vet_city.title()} (Within your {int(max_radius)}-mile preference)")
    elif dist is not None and dist <= max_radius * 2.0:
        score += 6
        loc_status = "warn"
        loc_detail = f"Regional ({dist:.0f} mi from {vet_city.title()}, {vet_state} — near {int(max_radius)} mi radius)"
        reasons.append(f"📍 Commute: Regional opportunity ({dist:.0f} miles from {vet_city.title()})")
    else:
        if relocate_ok:
            score += 4
            loc_status = "warn"
            loc_detail = f"Outside radius ({dist:.0f} mi from {vet_city.title()}, {vet_state} — Relocation match)" if dist else f"{job_loc_display} (Relocation match)"
        else:
            score -= 15
            loc_status = "fail"
            loc_detail = f"Outside {int(max_radius)} mi radius ({dist:.0f} mi from {vet_city.title()}, {vet_state})" if dist else f"{job_loc_display} (Outside radius)"

    # -------------------------------------------------------------------------
    # 6. MILITARY LEADERSHIP & MOS CROSSWALK (Max 10 pts Supportive Bonus)
    # -------------------------------------------------------------------------
    mos_info = lookup_mos(veteran_profile.get("mos", ""))
    if mos_info:
        mos_civilian_titles = [t.lower() for t in mos_info.get("civilian_titles", [])]
        if any(ct in job_title or job_title in ct for ct in mos_civilian_titles):
            score += 10
            reasons.append(f"Direct MOS Crosswalk: Aligns with {mos_info['title']} ({mos_info['branch']})")
        elif any(ts in job_text for ts in mos_info.get("transferable_skills", [])):
            score += 6
            reasons.append(f"Military Background Fit: {mos_info.get('branch')} specialty transferable skills")
        else:
            score += 3
    else:
        score += 2

    final_score = min(100.0, max(20.0, score))
    final_score = round(final_score, 1)

    # Self-improvement projected success math
    score_uplift = min(25.0, max(8.0, len(missing_skills) * 8.0)) if missing_skills else 8.0
    projected_score = min(98.0, round(final_score + score_uplift, 1))
    projected_salary_gain = min(30000, max(12000, len(missing_skills) * 6000)) if missing_skills else 12000

    factors = {
        "role_priority": role_priority,
        "role": {"label": "Role & Track Alignment", "status": role_status, "detail": role_detail, "is_custom_title_match": is_custom_match},
        "clearance": {"label": "Security Clearance", "status": clr_status, "detail": clr_detail, "eligible": clr_eligible},
        "skills": {"label": "Skills Alignment", "status": skills_status, "detail": skills_detail, "matched": matched_skills, "missing": missing_skills},
        "salary": {"label": "Compensation Range", "status": salary_status, "detail": salary_detail},
        "location": {"label": "Location & Travel Distance", "status": loc_status, "detail": loc_detail, "distance_miles": dist},
        "projected_score": projected_score,
        "score_delta": round(projected_score - final_score, 1),
        "projected_salary_gain": projected_salary_gain
    }

    return final_score, reasons, factors


# ============================================================================
# SIDEBAR: NAVIGATION, MULTI-BRANCH DEMO PROFILES & SYSTEM STATUS
# ============================================================================

with st.sidebar:
    st.image("https://img.shields.io/badge/7_Eagle_Group-Veteran_Placement-blue?style=for-the-badge&logo=shield")

    st.markdown("### 🎖️ Veteran Portal Navigation")
    nav_selection = st.radio(
        "Select Portal View:",
        ["📋 Veteran Intake & Match", "🗺️ MOS Career Crosswalk Explorer", "🦅 7 Eagle Group & Resources"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🚀 Fast Demo Profiles")
    st.markdown("Test the pipeline across different military specialties in **1 click**:")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if st.button("🪖 18F SF Lead", use_container_width=True, help="Army Special Forces / Cloud Architect"):
            p = DEMO_VETERAN_PROFILES["18F"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.session_state["pipeline_executed"] = False
            st.toast("✅ Loaded Army 18F Special Forces Profile!", icon="🎖️")
            st.rerun()

        if st.button("🪖 88M Logistics", use_container_width=True, help="Army Motor Transport & CDL"):
            p = DEMO_VETERAN_PROFILES["88M"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.session_state["pipeline_executed"] = False
            st.toast("✅ Loaded Army 88M Logistics Profile!", icon="🎖️")
            st.rerun()

    with col_d2:
        if st.button("🪖 11B Infantry", use_container_width=True, help="Army Infantry Squad Leader"):
            p = DEMO_VETERAN_PROFILES["11B"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.session_state["pipeline_executed"] = False
            st.toast("✅ Loaded Army 11B Infantry Profile!", icon="🎖️")
            st.rerun()

        if st.button("⚓ Navy IT / Cyber", use_container_width=True, help="Navy IT Systems Administrator"):
            p = DEMO_VETERAN_PROFILES["25B"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.session_state["pipeline_executed"] = False
            st.toast("✅ Loaded Navy IT Profile!", icon="🎖️")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Live Platform Impact")
    st.markdown(f"""
    <div style="background: white; border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.85rem; margin-bottom: 0.75rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.85rem; color: #475569;">👥 <strong>Total Visits:</strong></span>
            <span style="background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 0.88rem; padding: 0.15rem 0.5rem; border-radius: 6px;">{platform_metrics['total_visitors']:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.85rem; color: #475569;">⚡ <strong>AI Matches Run:</strong></span>
            <span style="background: #dcfce7; color: #166534; font-weight: 700; font-size: 0.88rem; padding: 0.15rem 0.5rem; border-radius: 6px;">{platform_metrics['total_matches_run']:,}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.85rem; color: #475569;">🦅 <strong>Recruiter Intros:</strong></span>
            <span style="background: #fef3c7; color: #92400e; font-weight: 700; font-size: 0.88rem; padding: 0.15rem 0.5rem; border-radius: 6px;">{platform_metrics['veterans_connected']:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Engine Status")
    if SPARK_AVAILABLE:
        st.success("🟢 Databricks Serverless Active\n\nConnected to Unity Catalog")
    else:
        st.info("🔵 Zero-Cost Free Tier / Local\n\nRunning in local mode with 100% free resume parsing & job matching")

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.82rem; color: #64748b; text-align: center; line-height: 1.45;'>
            <strong>For Your Service</strong><br>
            Universal Veteran Career Platform<br>
            <strong>Free Hall</strong><br>
            <em>Cloud Engineer • DevOps Analyst • Data Architect</em><br>
            <em>18Z / 18F US Army Special Forces (Ret.)</em>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================================
# HERO BANNER & PROMINENT VISITOR / IMPACT COUNTER BAR
# ============================================================================

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title" style="display: flex; align-items: center; flex-wrap: wrap; gap: 12px;">
        <img src="https://flagcdn.com/w80/us.png" srcset="https://flagcdn.com/w160/us.png 2x" width="46" height="30" alt="United States Flag" style="border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.35); vertical-align: middle; display: inline-block;">
        <span>FOR YOUR SERVICE</span>
    </div>
    <div class="hero-subtitle" style="font-size: 1.15rem; font-weight: 700; color: #facc15; margin-top: 4px;">Veteran Career Transition Intelligence</div>
    <div style="font-size: 0.95rem; color: #e2e8f0; margin-top: 6px; font-style: italic; max-width: 780px;">"Your transition generates thousands of service data points every day. We turn that data into a clear path forward."</div>
    <div class="hero-badge" style="margin-top: 8px;">🎖️ Serving ALL Branches • 100% Free Veteran Transition Platform</div>
</div>

<div style="background: linear-gradient(135deg, #0b1d3a 0%, #1e3a8a 100%); border-radius: 12px; padding: 1.15rem; margin: 1rem 0 1.25rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.12); color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; text-align: center;">
        <div style="flex: 1; min-width: 130px; padding: 0.6rem 0.5rem; background: rgba(255,255,255,0.08); border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);">
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #93c5fd; font-weight: 700;">👥 Platform Visitors</div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #ffffff; margin-top: 2px;">{platform_metrics['total_visitors']:,}</div>
            <div style="font-size: 0.72rem; color: #cbd5e1; margin-top: 2px;">Live Visitor Counter</div>
        </div>
        <div style="flex: 1; min-width: 130px; padding: 0.6rem 0.5rem; background: rgba(255,255,255,0.08); border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);">
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #86efac; font-weight: 700;">⚡ AI Matches Run</div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #4ade80; margin-top: 2px;">{platform_metrics['total_matches_run']:,}</div>
            <div style="font-size: 0.72rem; color: #cbd5e1; margin-top: 2px;">Profiles Evaluated</div>
        </div>
        <div style="flex: 1; min-width: 130px; padding: 0.6rem 0.5rem; background: rgba(255,255,255,0.08); border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);">
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #fde047; font-weight: 700;">🦅 Recruiter Intros</div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #facc15; margin-top: 2px;">{platform_metrics['veterans_connected']:,}</div>
            <div style="font-size: 0.72rem; color: #cbd5e1; margin-top: 2px;">7 Eagle Placements</div>
        </div>
        <div style="flex: 1; min-width: 130px; padding: 0.6rem 0.5rem; background: rgba(255,255,255,0.08); border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);">
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #f472b6; font-weight: 700;">💼 Active Job Roles</div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #f43f5e; margin-top: 2px;">250+</div>
            <div style="font-size: 0.72rem; color: #cbd5e1; margin-top: 2px;">USAJOBS & Industry</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# VIEW 1: UNIVERSAL VETERAN INTAKE & MATCHING
# ============================================================================

if nav_selection == "📋 Veteran Intake & Match":

    # Responsive Branch Insignia Grid
    st.markdown("""
    <div class="branch-grid">
        <div class="branch-card"><strong>🪖 U.S. Army</strong><br><small>All MOS Specialties</small></div>
        <div class="branch-card"><strong>⚓ U.S. Navy</strong><br><small>All Ratings</small></div>
        <div class="branch-card"><strong>✈️ U.S. Air Force</strong><br><small>All AFSCs</small></div>
        <div class="branch-card"><strong>🦅 U.S. Marine Corps</strong><br><small>All MOS Codes</small></div>
        <div class="branch-card"><strong>🚢 U.S. Coast Guard</strong><br><small>All Maritime Ratings</small></div>
        <div class="branch-card"><strong>🚀 U.S. Space Force</strong><br><small>All Space & Cyber</small></div>
    </div>
    """, unsafe_allow_html=True)

    # Mission Statement & Value Comparison
    with st.expander("🎖️ The Mission & What For Your Service Does (Why We Built This)", expanded=False):
        st.markdown("""
        **The Mission**
        The military gives you elite operational experience. Civilian tech applications don't always know how to read it. Raw service records, MOS codes, and leadership tours sit in static PDFs rather than working for you. **For Your Service** learns the patterns in your background, maps your service profile against live industry demand, and surfaces what matters: targeted role matching, resume translation, and automated transition insights.

        ---

        **What For Your Service Does**

        | Without For Your Service | With For Your Service |
        | :--- | :--- |
        | Translating your military experience into resume bullet points is manual and frustrating | Automated MOS/AFSC-to-industry role mapping and tensor matching |
        | Federal and defense job boards are scattered and hard to track | Live integrated USAJOBS and defense contractor feed ingestion |
        | Finding the right technical team or mentor is a guessing game | Data-driven introductions based on peer transition paths |
        | Tracking your application pipeline is messy | Unified pipeline tracking through Databricks and a local dashboard |
        """)

    with st.expander("⚙️ Distributed Lakehouse & Telemetry Architecture (System Specification)", expanded=False):
        st.markdown("""
        ### Distributed Telemetry & Feature Engineering Pipeline Architecture

        The platform processes high-volume, disparate operational payloads, enforcing strict enterprise-grade data governance and feeding downstream vector-matching and AI inference engines:

        #### 1. Fault-Tolerant Telemetry Ingestion
        * **Implementation:** Built on PySpark and Delta Lake to process continuous, unstructured and structured operational data streams with zero data-loss guarantees.
        * **Resilience:** Designed to handle high-throughput payloads, parsing complex state transitions and malformed payloads reliably at scale via Dead Letter Queue (DLQ) quarantine.

        #### 2. Enterprise Governance & Metadata Management
        * **Implementation:** Leverages Databricks Unity Catalog for centralized access control, lineage tracking, and fine-grained permissions across multi-cloud environments.
        * **Compliance:** Enforces strict metadata boundaries, column/row-level access control (RBAC/ABAC), and immutable audit logs across multi-tier storage layers.

        #### 3. ML Feature Store & Vector Matching
        * **Implementation:** Transforms raw ingested payloads into high-dimensional vectorized representations (384-dimensional dense tensors) using distributed PySpark `@pandas_udf` batch inference.
        * **Application:** Feeds automated vector-matching and feature engineering pipelines designed for real-time similarity scoring and analytical modeling.

        #### 4. Operational Observability Control Plane
        * **Implementation:** Streamlit-based interface hosted natively on Databricks Apps providing real-time visibility into pipeline throughput, data freshness decay curves, and model telemetry for technical stakeholders.
        """)

    with st.expander("🛡️ Dynamic Veteran Talent Recon Grid & LinkedIn X-Ray Engine", expanded=False):
        st.markdown("""
        ### 🔍 Dynamic Personnel Reconnaissance & X-Ray Search Launcher
        Enter **any company, position, and location** to instantly filter military veteran profiles from our talent ledger and generate targeted **Google/DuckDuckGo Boolean X-Ray search vectors** for live LinkedIn profiles.
        """)
        
        li_col1, li_col2, li_col3 = st.columns(3)
        with li_col1:
            li_company = st.text_input("Target Company / Organization", value="GE Aerospace", help="e.g. GE Aerospace, Lockheed Martin, AWS, SpaceX", key="li_dyn_comp")
        with li_col2:
            li_role = st.text_input("Target Position / Role", value="Sr AI Data Engineer", help="e.g. Sr AI Data Engineer, Cloud Architect, Systems Engineer", key="li_dyn_role")
        with li_col3:
            li_loc = st.text_input("Target Location / Region", value="Greenville, SC", help="e.g. Greenville, SC, Huntsville, AL, Remote", key="li_dyn_loc")
            
        if LinkedInVeteranFinder:
            finder_inst = LinkedInVeteranFinder(company=li_company, role=li_role, location=li_loc)
            b_query = finder_inst.generate_boolean_query()
            g_url = finder_inst.generate_google_search_url()
            d_url = finder_inst.generate_duckduckgo_url()
            l_url = finder_inst.generate_direct_linkedin_search_url()
            ledger_matches = finder_inst.search_talent_ledger(veteran_only=True)
            
            recon_tab1, recon_tab2, recon_tab3 = st.tabs(["🛰️ Personnel Recon Results", "📡 Live Web X-Ray Search", "💬 Warm Outreach Generator"])
            
            with recon_tab1:
                st.markdown(f"**Acquired Targets in Talent Ledger ({len(ledger_matches)} found):**")
                if not ledger_matches.empty:
                    st.dataframe(ledger_matches[['name', 'company', 'title', 'location', 'branch', 'clearance', 'skills']], use_container_width=True)
                else:
                    st.info(f"No internal ledger matches for '{li_company}' / '{li_role}' / '{li_loc}'. Use the Live Web X-Ray tab to search external LinkedIn profiles!")
                    
            with recon_tab2:
                st.markdown("**Formulated Boolean X-Ray Query (Public Indexed Profiles):**")
                st.code(b_query, language="text")
                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    st.link_button("🚀 Launch Google X-Ray", g_url, use_container_width=True)
                with b_col2:
                    st.link_button("🦆 Launch DuckDuckGo X-Ray", d_url, use_container_width=True)
                with b_col3:
                    st.link_button("🔗 Direct LinkedIn Search", l_url, use_container_width=True)
                    
            with recon_tab3:
                p_msg = finder_inst.generate_peer_outreach_message(peer_name="Alex", sender_name="Free Hall", sender_branch="US Army Special Forces (18F / 18Z, Ret.)", target_role=li_role)
                m_msg = finder_inst.generate_hiring_manager_outreach_message(manager_name="Hiring Team Lead", sender_name="Free Hall", target_role=li_role)
                out_tab1, out_tab2 = st.tabs(["Veteran Peer-to-Peer Message", "Hiring Manager Executive Outreach"])
                with out_tab1:
                    st.text_area("Peer Outreach Message (Ready to Copy)", value=p_msg, height=160, key="li_peer_msg_dyn")
                with out_tab2:
                    st.text_area("Executive Outreach Message (Ready to Copy)", value=m_msg, height=160, key="li_mgr_msg_dyn")

    # Mobile & Quick Demo Selector (Accessible on all screens)
    with st.expander("⚡ 1-Click Fast Demo Profiles (Tap to auto-fill for testing)"):
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            if st.button("🪖 18F SF Lead", key="mob_demo_18f", use_container_width=True, help="Army Special Forces / Cloud Architect"):
                p = DEMO_VETERAN_PROFILES["18F"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.session_state["pipeline_executed"] = False
                st.toast("✅ Loaded Army 18F Special Forces Profile!", icon="🎖️")
                st.rerun()
        with m_col2:
            if st.button("🪖 11B Infantry", key="mob_demo_11b", use_container_width=True, help="Army Infantry Squad Leader"):
                p = DEMO_VETERAN_PROFILES["11B"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.session_state["pipeline_executed"] = False
                st.toast("✅ Loaded Army 11B Infantry Profile!", icon="🎖️")
                st.rerun()
        with m_col3:
            if st.button("🪖 88M Logistics", key="mob_demo_88m", use_container_width=True, help="Army Motor Transport & CDL"):
                p = DEMO_VETERAN_PROFILES["88M"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.session_state["pipeline_executed"] = False
                st.toast("✅ Loaded Army 88M Logistics Profile!", icon="🎖️")
                st.rerun()
        with m_col4:
            if st.button("⚓ Navy IT / Cyber", key="mob_demo_it", use_container_width=True, help="Navy IT Systems Administrator"):
                p = DEMO_VETERAN_PROFILES["25B"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.session_state["pipeline_executed"] = False
                st.toast("✅ Loaded Navy IT Profile!", icon="🎖️")
                st.rerun()

    st.markdown("")

    # ------------------------------------------------------------------------
    # STEP 1: RESUME UPLOAD CENTER (CENTERPIECE OF INTAKE)
    # ------------------------------------------------------------------------
    st.markdown("### 📄 Step 1: Upload Your Military Resume / Service Record")
    st.markdown(
        "Upload your resume in **PDF, Word (.docx), or Text (.txt)** format. "
        "Our free AI parser will automatically extract your technical skills, leadership qualifications, "
        "and military accomplishments to match you with top civilian opportunities."
    )

    uploaded_file = st.file_uploader(
        "Choose a Resume File (.pdf, .docx, .txt)",
        type=["pdf", "docx", "txt"],
        help="Upload your civilian resume, military VMET, or ERB/ORB record"
    )

    resume_content = st.session_state.get("form_resume_text", "")
    if uploaded_file is not None:
        extracted_text = extract_text_from_file(uploaded_file)
        if extracted_text:
            resume_content = extracted_text
            st.session_state["form_resume_text"] = extracted_text
            st.success(f"✅ Successfully parsed `{uploaded_file.name}` ({len(extracted_text):,} characters extracted)")

    # ------------------------------------------------------------------------
    # STEP 2: MILITARY SERVICE & CLEARANCE DETAILS
    # ------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🎖️ Step 2: Military Background & Security Clearance")

    col_b1, col_b2, col_b3 = st.columns(3)

    with col_b1:
        branches = ["Army", "Navy", "Air Force", "Marine Corps", "Coast Guard", "Space Force"]
        branch_default_idx = 0
        if "form_branch" in st.session_state and st.session_state["form_branch"] in branches:
            branch_default_idx = branches.index(st.session_state["form_branch"])

        selected_branch = st.selectbox(
            "Military Service Branch *",
            branches,
            index=branch_default_idx,
            key="branch_selector",
            help="Select the military branch you served in"
        )

    # Dynamic Ranks for the selected branch
    with col_b2:
        available_ranks = BRANCH_RANKS.get(selected_branch, BRANCH_RANKS["Army"])
        rank_default_idx = 0
        if "form_rank" in st.session_state:
            for idx, r in enumerate(available_ranks):
                if st.session_state["form_rank"].split("|")[0].strip() in r:
                    rank_default_idx = idx
                    break

        selected_rank = st.selectbox(
            f"Rank / Pay Grade ({selected_branch}) *",
            available_ranks,
            index=rank_default_idx,
            help="Select your current or separation rank"
        )

    with col_b3:
        service_statuses = [
            "Active Duty (Transitioning / ETS soon)",
            "Veteran (Separated / Discharged)",
            "Veteran (Retired)",
            "National Guard / Reserve",
            "Military Spouse / Family"
        ]
        status_default_idx = 0
        if "form_service_status" in st.session_state:
            for idx, s in enumerate(service_statuses):
                if st.session_state["form_service_status"] in s:
                    status_default_idx = idx
                    break

        selected_status = st.selectbox(
            "Service Status *",
            service_statuses,
            index=status_default_idx
        )

    # MOS / Specialty & Security Clearance
    col_m1, col_m2 = st.columns([1, 1])

    with col_m1:
        mos_default = st.session_state.get("form_mos", "")
        mos_input = st.text_input(
            "MOS / AFSC / Rating Code or Role Title *",
            value=mos_default,
            placeholder="e.g., 11B, 18F, 88M, 92Y, 68W, IT, CTN, 1D7X1, 0311, BM...",
            help="Enter your military occupational code or duty title"
        ).strip().upper()

        # Real-time MOS crosswalk preview
        if mos_input:
            mos_info = lookup_mos(mos_input)
            if mos_info:
                st.info(
                    f"**🎖️ Military Specialty Identified:** `{mos_input}` — **{mos_info['title']}** ({mos_info['branch']})\n\n"
                    f"• **Civilian Equivalents:** {', '.join(mos_info['civilian_titles'][:3])}\n\n"
                    f"• **Key Transferable Skills:** {', '.join(mos_info['transferable_skills'][:5])}"
                )

    with col_m2:
        clearance_options = [
            "None / Public Trust",
            "Confidential",
            "Secret",
            "Top Secret",
            "Top Secret / SCI",
            "TS / SCI with CI Poly",
            "TS / SCI with Full Scope Poly"
        ]
        clr_default_idx = 0
        if "form_clearance" in st.session_state:
            for idx, c in enumerate(clearance_options):
                if st.session_state["form_clearance"] in c:
                    clr_default_idx = idx
                    break

        selected_clearance = st.selectbox(
            "Active Security Clearance Level *",
            clearance_options,
            index=clr_default_idx,
            help="Select your highest active or recent security clearance"
        )

    # ------------------------------------------------------------------------
    # STEP 3: CONTACT & TARGET CIVILIAN PREFERENCES
    # ------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📋 Step 3: Contact Info & Civilian Career Targets")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        name_default = st.session_state.get("form_name", "")
        full_name = st.text_input("Full Name *", value=name_default, placeholder="e.g., John Miller")
        if full_name:
            st.session_state["form_name"] = full_name
    with col_c2:
        email_default = st.session_state.get("form_email", "")
        email_addr = st.text_input("Email Address *", value=email_default, placeholder="veteran@example.com")
        if email_addr:
            st.session_state["form_email"] = email_addr
    with col_c3:
        phone_default = st.session_state.get("form_phone", "")
        phone_num = st.text_input("Phone Number", value=phone_default, placeholder="(555) 123-4567")
        if phone_num:
            st.session_state["form_phone"] = phone_num

    col_t1, col_t2, col_t3 = st.columns([1.2, 0.8, 1.2])
    with col_t1:
        city_default = st.session_state.get("form_target_city", "")
        target_city = st.text_input("Target City / Metro *", value=city_default, placeholder="e.g., Dallas, Greenville, Tampa, San Diego, Fayetteville...").strip()
        if target_city:
            st.session_state["form_target_city"] = target_city
    with col_t2:
        state_default = st.session_state.get("form_target_state", "")
        target_state = st.text_input("Target State (2-letter code) *", value=state_default, max_chars=2, placeholder="e.g., TX, SC, FL, CA, NC...").strip().upper()
        if target_state:
            st.session_state["form_target_state"] = target_state
    with col_t3:
        radius_options = ["10 miles", "20 miles", "50 miles", "100 miles", "Any Distance / Nationwide"]
        radius_default_idx = 2  # 50 miles
        if "form_target_radius" in st.session_state and st.session_state["form_target_radius"] in radius_options:
            radius_default_idx = radius_options.index(st.session_state["form_target_radius"])
        target_radius = st.selectbox(
            "Max Commute / Travel Radius *",
            radius_options,
            index=radius_default_idx,
            help="Choose maximum travel distance from city center: 10 miles, 20 miles, 50 miles, 100 miles, etc."
        )
        st.session_state["form_target_radius"] = target_radius

    col_flex1, col_flex2 = st.columns(2)
    with col_flex1:
        remote_ok = st.checkbox("Open to Remote / Hybrid Opportunities", value=st.session_state.get("form_remote_ok", True))
        st.session_state["form_remote_ok"] = remote_ok
    with col_flex2:
        relocate_ok = st.checkbox("Willing to Relocate for the Right Opportunity", value=st.session_state.get("form_relocate", True))
        st.session_state["form_relocate"] = relocate_ok

    # Target Career Track Selection
    col_track1, col_track2 = st.columns([1, 1])
    with col_track1:
        track_options = list(CAREER_TRACKS.keys())
        track_default_idx = 0
        if "form_career_track" in st.session_state and st.session_state["form_career_track"] in track_options:
            track_default_idx = track_options.index(st.session_state["form_career_track"])

        selected_career_track = st.selectbox(
            "🎯 Primary Target Career Field / Industry Track *",
            track_options,
            index=track_default_idx,
            help="Choose the civilian career track you want to target so we can analyze skill gaps and recommend certifications"
        )
    with col_track2:
        desired_role_custom = st.text_input(
            "Specific Desired Job Title(s) (Optional)",
            value=st.session_state.get("form_desired_role", ""),
            placeholder="e.g., Solutions Architect, Operations Supervisor, Fleet Dispatcher, Site Superintendent...",
            help="Enter any specific job titles you are looking for"
        )

    col_sal1, col_sal2 = st.columns(2)
    with col_sal1:
        sal_min_default = st.session_state.get("form_salary_min", 70000)
        salary_min = st.slider(
            "Minimum Desired Annual Salary ($)",
            min_value=35000,
            max_value=220000,
            value=int(sal_min_default),
            step=5000,
            format="$%d"
        )
    with col_sal2:
        sal_max_default = st.session_state.get("form_salary_max", 130000)
        salary_max = st.slider(
            "Target / Ceiling Annual Salary ($)",
            min_value=45000,
            max_value=250000,
            value=int(sal_max_default),
            step=5000,
            format="$%d"
        )

    # Resume Text Area (Editable & Auto-Populated)
    st.markdown("#### 📝 Resume / Military Summary Text")
    resume_text = st.text_area(
        "Resume Text (Auto-filled if file uploaded above, or paste here) *",
        value=resume_content,
        height=220,
        placeholder="Paste your complete resume, military evaluation bullets, awards, specialties, and experience here...\n\nExample:\n- Commanded 9-person squad in high-tempo field operations\n- Maintained 100% accountability for $1.5M in sensitive equipment\n- Supervised preventive maintenance, safety audits, and operational readiness"
    )

    st.markdown("")
    launch_btn = st.button("🚀 Launch AI Matching Pipeline & Career Optimizer", use_container_width=True)

    # ------------------------------------------------------------------------
    # EXECUTION: AI MATCHING PIPELINE
    # ------------------------------------------------------------------------
    if launch_btn:
        print(f"[PIPELINE START] Name: '{full_name}', Email: '{email_addr}', Branch: '{selected_branch}', Rank: '{selected_rank}', MOS: '{mos_input}', Clearance: '{selected_clearance}', Location: '{target_city}, {target_state}'")
        if not full_name or not email_addr or not target_city or not target_state or not resume_text:
            print("[PIPELINE VALIDATION ERROR] Missing required fields")
            st.error("🚨 Please fill out all required fields (*) or upload a resume before launching the pipeline.")
        elif len(target_state) != 2:
            print(f"[PIPELINE VALIDATION ERROR] Invalid state code: '{target_state}'")
            st.error("🚨 Target State must be a 2-letter state code (e.g., SC, NC, FL, TX, GA, VA).")
        elif salary_min >= salary_max:
            print(f"[PIPELINE VALIDATION ERROR] Salary min ({salary_min}) >= max ({salary_max})")
            st.error("🚨 Minimum desired salary must be less than the target salary.")
        elif len(resume_text.strip()) < 50:
            print(f"[PIPELINE VALIDATION ERROR] Resume text too short ({len(resume_text.strip())} chars)")
            st.error("🚨 Resume text is too short. Please provide a complete resume or military summary (at least 50 characters).")
        else:
            get_platform_metrics(increment_match=True)
            with st.spinner("⚡ Setting AI pipeline in motion: Parsing military experience, evaluating MOS crosswalk, and matching jobs..."):
                veteran_id = str(uuid.uuid4())
                print(f"[PIPELINE] Processing veteran_id: {veteran_id}")

                # 1. Parse Skills
                print(f"[PIPELINE] Parsing skills from resume ({len(resume_text)} chars) with MOS '{mos_input}'...")
                extracted = parse_veteran_skills(resume_text, mos_input)
                print(f"[PIPELINE] Extracted {len(extracted.get('technical_skills', []))} tech skills, {len(extracted.get('leadership_skills', []))} leadership skills, {len(extracted.get('ops_skills', []))} ops skills. Seniority: {extracted.get('seniority')}")

                # 2. Build Veteran Profile Object
                veteran_profile = {
                    "veteran_id": veteran_id,
                    "name": full_name,
                    "email": email_addr,
                    "phone": phone_num,
                    "branch": selected_branch,
                    "rank": selected_rank,
                    "mos": mos_input,
                    "clearance": selected_clearance,
                    "service_status": selected_status,
                    "target_track": selected_career_track,
                    "desired_role": desired_role_custom,
                    "target_city": target_city,
                    "target_state": target_state,
                    "target_radius": target_radius,
                    "remote_ok": remote_ok,
                    "relocate": relocate_ok,
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "total_years": extracted["total_years"],
                    "seniority": extracted["seniority"],
                    "technical_skills": extracted["technical_skills"],
                    "leadership_skills": extracted["leadership_skills"],
                    "ops_skills": extracted["ops_skills"]
                }

                # 3. Store in Unity Catalog if Spark is available
                if SPARK_AVAILABLE and spark:
                    try:
                        print("[PIPELINE] Writing veteran profile to Unity Catalog: workspace.fys_silver.veteran_profiles...")
                        profile_df = spark.createDataFrame([{
                            "veteran_id": veteran_id,
                            "name": full_name,
                            "email": email_addr,
                            "branch": selected_branch,
                            "rank": selected_rank,
                            "mos_code": mos_input,
                            "clearance": selected_clearance,
                            "target_city": target_city,
                            "target_state": target_state,
                            "total_years": extracted["total_years"],
                            "seniority_level": extracted["seniority"],
                            "technical_skills": json.dumps(extracted["technical_skills"]),
                            "salary_min": salary_min,
                            "salary_max": salary_max,
                            "created_at": datetime.now()
                        }])
                        profile_df.write.format("delta").mode("append").saveAsTable("workspace.fys_silver.veteran_profiles")
                        print("[PIPELINE] Successfully wrote profile to Unity Catalog")
                    except Exception as e:
                        print(f"[PIPELINE WARNING] Unity Catalog write skipped/failed: {e}")

                # 4. Load Job Postings & Compute Semantic Matches (Location & Track Aware)
                all_jobs = load_cached_scraped_jobs(target_city=target_city, target_state=target_state, target_track=selected_career_track)
                print(f"[PIPELINE] Loaded {len(all_jobs)} candidate job postings for {target_city}, {target_state}. Running scoring engine...")
                matches = []
                for job in all_jobs:
                    score, reasons, factors = calculate_veteran_match_score(job, veteran_profile, extracted)
                    # Filter out disallowed cross-domain jobs from primary results
                    if factors.get("role_priority", 5) < 90:
                        matches.append({
                            **job,
                            "match_score": score,
                            "match_reasons": reasons,
                            "factors": factors
                        })

                # Sort by:
                # 1. role_priority (1: direct requested title match, 2: keyword match, 3: target track match)
                # 2. clearance eligibility (eligible first)
                # 3. match_score descending
                def match_sort_key(item):
                    f = item.get("factors", {})
                    prio = f.get("role_priority", 5)
                    clr_pass = 1 if f.get("clearance", {}).get("status") == "pass" else 0
                    return (prio, -clr_pass, -item["match_score"])

                matches = sorted(matches, key=match_sort_key)
                print(f"[PIPELINE COMPLETE] Generated {len(matches)} ranked matches for {full_name}. Top match: '{matches[0]['title'] if matches else 'N/A'}' ({matches[0]['match_score'] if matches else 0}%)")

                # 5. Compute Career Readiness & Skill Gap Analysis
                all_user_skills = extracted["technical_skills"] + extracted["leadership_skills"] + extracted["ops_skills"] + extracted.get("mos_skills", [])
                top_score = matches[0]["match_score"] if matches else 70.0
                readiness_data = analyze_career_readiness(selected_career_track, all_user_skills, top_score)

                # Save to session state
                st.session_state["pipeline_executed"] = True
                st.session_state["current_matches"] = matches
                st.session_state["current_profile"] = veteran_profile
                st.session_state["current_extracted"] = extracted
                st.session_state["current_readiness"] = readiness_data
                st.toast("✅ AI Matching & Skill Gap Analysis complete!", icon="🎯")

    # ------------------------------------------------------------------------
    # OUTPUT: COMPREHENSIVE VETERAN TRANSITION DASHBOARD
    # ------------------------------------------------------------------------
    if st.session_state.get("pipeline_executed") and "current_matches" in st.session_state:
        matches = st.session_state["current_matches"]
        profile = st.session_state["current_profile"]
        extracted = st.session_state["current_extracted"]
        readiness = st.session_state.get("current_readiness", {})

        st.markdown("---")
        st.markdown(f"## 🎯 Career Match Results for **{profile['name']}**")

        # Profile Summary Badge
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; padding: 1.25rem; border: 1px solid #cbd5e1; margin-bottom: 1.25rem; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div><strong>Branch:</strong> {profile['branch']}</div>
                <div><strong>Rank:</strong> {profile['rank']}</div>
                <div><strong>Specialty:</strong> {profile['mos']}</div>
                <div><span class="clearance-badge">🛡️ {profile['clearance']}</span></div>
                <div><strong>Target Track:</strong> {profile.get('target_track', 'Operations')}</div>
                <div><strong>Experience:</strong> {profile['seniority']} (~{extracted['total_years']} yrs)</div>
                <div><strong>Target:</strong> {profile['target_city']}, {profile['target_state']} ({profile.get('target_radius', '50 miles')} radius) (${profile['salary_min']:,.0f} - ${profile['salary_max']:,.0f})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Extracted Skills & Verification Display
        st.markdown("#### 🔍 Candidate Skills & Military Experience Breakdown")

        col_sk1, col_sk2 = st.columns(2)
        with col_sk1:
            st.markdown("**📄 Verified Skills Detected in Resume:**")
            resume_skills = extracted["technical_skills"] + extracted["ops_skills"] + extracted["leadership_skills"]
            if resume_skills:
                skills_html = ""
                for s in extracted["technical_skills"][:8]:
                    skills_html += f"<span class='skill-chip'>💻 {s.upper()}</span> "
                for o in extracted["ops_skills"][:6]:
                    skills_html += f"<span class='ops-skill-chip'>⚙️ {o.title()}</span> "
                for l in extracted["leadership_skills"][:6]:
                    skills_html += f"<span class='mil-skill-chip'>🎖️ {l.title()}</span> "
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No specific technical keywords detected in resume text. The matching engine is using your verified military experience, rank, clearance, and target career track.")

        with col_sk2:
            st.markdown(f"**🪖 Military Specialty Crosswalk ({profile['branch']} {profile['mos']}):**")
            if extracted.get("mos_skills"):
                mos_html = ""
                for m in extracted["mos_skills"][:6]:
                    mos_html += f"<span class='mil-skill-chip'>🪖 {m.title()}</span> "
                st.markdown(mos_html, unsafe_allow_html=True)
            else:
                st.markdown(f"*General Military Service — {profile['branch']}*")

        st.markdown("")

        # 1-CLICK PDF TRANSITION BRIEF & RESUME EXPORT ACTION BAR
        col_pdf1, col_pdf2 = st.columns([1.5, 1])
        with col_pdf1:
            try:
                pdf_payload = generate_veteran_transition_pdf(
                    candidate_info=profile,
                    extracted_skills=extracted,
                    matches=matches,
                    readiness=readiness,
                    mos_info=mos_info
                )
                clean_filename = f"Transition_Brief_{full_name.strip().replace(' ', '_')}_{profile['mos']}.pdf"
                st.download_button(
                    label="📄 📥 Download Transition Intelligence Brief (PDF)",
                    data=pdf_payload,
                    file_name=clean_filename,
                    mime="application/pdf",
                    use_container_width=True,
                    help="Download an executive-grade transition report and matched civilian opportunities formatted for recruiters, hiring managers, and corporate partner introductions."
                )
            except Exception as e:
                st.caption(f"💡 PDF Brief generation ready ({e})")
        with col_pdf2:
            st.markdown(
                '<div style="text-align: right; padding-top: 6px;">'
                '<span style="background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 0.85rem; padding: 0.35rem 0.75rem; border-radius: 6px;">'
                '🛡️ 7 Eagle Certified Brief'
                '</span></div>',
                unsafe_allow_html=True
            )

        st.markdown("")

        # TABS: JOB MATCHES vs CAREER READINESS & SKILL GAP OPTIMIZER
        tab_jobs, tab_readiness = st.tabs([
            f"💼 Top Matching Opportunities ({len(matches[:8])})",
            f"🚀 Career Readiness & Skill Gap Optimizer ({readiness.get('target_track', 'Target Track')})"
        ])

        with tab_jobs:
            st.markdown("### 💼 Top Matching Opportunities")
            top_matches = matches[:8]

            if not top_matches:
                st.markdown(f"""
                <div style="background: #eff6ff; border: 1px solid #93c5fd; border-radius: 8px; padding: 1.75rem; text-align: center; margin: 1rem 0;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
                    <h4 style="color: #1e3a8a; margin: 0 0 0.5rem 0;">No Active Live Positions in Immediate Commute Radius</h4>
                    <p style="color: #475569; font-size: 0.95rem; margin-bottom: 0.75rem;">
                        No open positions are currently active within your strict {profile.get('target_radius', '50 miles')} radius in <strong>{profile.get('target_city', 'your area')}, {profile.get('target_state', '')}</strong>.
                    </p>
                    <p style="color: #1e40af; font-weight: 600; font-size: 0.9rem; margin: 0;">
                        💡 Recommendation: Check <strong>'Open to Remote Work'</strong> or expand your commute radius to 50–100 miles in the intake form to unlock nationwide defense and commercial opportunities.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            for idx, job in enumerate(top_matches, 1):
                score = job["match_score"]
                badge_class = "match-badge-high" if score >= 75 else "match-badge-med"
                factors = job.get("factors", {})

                clr_req = job.get('clearance_required', 'None')
                clr_is_fail = factors.get("clearance", {}).get("status") == "fail"

                # Outbound Application URL with Official Referral Attribution
                raw_url = str(job.get("application_url") or job.get("url") or "")
                if not raw_url or raw_url == "#" or not raw_url.startswith("http"):
                    co_q = str(job.get("company", "")).replace(" ", "+")
                    ti_q = str(job.get("title", "")).replace(" ", "+")
                    app_url = f"https://www.google.com/search?q={co_q}+{ti_q}+careers+jobs"
                else:
                    app_url = raw_url.replace(":443", "")
                    if "usajobs.gov" in app_url and "utm_source" not in app_url:
                        sep = "&" if "?" in app_url else "?"
                        app_url = f"{app_url}{sep}utm_source=for_your_service&utm_medium=veteran_platform&utm_campaign=7_eagle_group"

                # Sanitize all string fields to prevent broken/unclosed HTML tags
                card_title = re.sub(r'<[^>]+>', '', str(job.get('title', 'Untitled Role'))).strip()
                card_company = re.sub(r'<[^>]+>', '', str(job.get('company', 'Employer'))).strip()
                card_location = re.sub(r'<[^>]+>', '', str(job.get('location_display', 'Location'))).strip()
                raw_desc = re.sub(r'<[^>]+>', ' ', str(job.get('description', ''))).strip()
                raw_desc = re.sub(r'\s+', ' ', raw_desc)
                card_desc = raw_desc[:320] + ("..." if len(raw_desc) > 320 else "")

                prio = factors.get("role_priority", 5)
                is_custom_req = factors.get("role", {}).get("is_custom_title_match", False)
                prio_badge = ""
                if prio == 1:
                    if is_custom_req:
                        prio_badge = '&nbsp;<span style="background: #fef08a; color: #854d0e; font-weight: 700; font-size: 0.82rem; padding: 0.2rem 0.5rem; border-radius: 6px;">🎯 Requested Title Match</span>'
                    else:
                        prio_badge = '&nbsp;<span style="background: #dcfce7; color: #166534; font-weight: 700; font-size: 0.82rem; padding: 0.2rem 0.5rem; border-radius: 6px;">🎯 Target Career Track</span>'
                elif prio == 2:
                    prio_badge = '&nbsp;<span style="background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 0.82rem; padding: 0.2rem 0.5rem; border-radius: 6px;">🎯 Requested Keyword Match</span>'
                elif prio == 3:
                    prio_badge = '&nbsp;<span style="background: #ede9fe; color: #5b21b6; font-weight: 700; font-size: 0.82rem; padding: 0.2rem 0.5rem; border-radius: 6px;">🎯 Requested Role Specialty</span>'
                elif prio == 4:
                    prio_badge = '&nbsp;<span style="background: #dcfce7; color: #166534; font-weight: 700; font-size: 0.82rem; padding: 0.2rem 0.5rem; border-radius: 6px;">🎯 Target Career Track</span>'

                with st.container():
                    st.markdown(f"""
                    <div class="job-card" style="border-left: 6px solid {'#dc2626' if clr_is_fail else '#0b2545'};">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 8px;">
                            <div style="flex: 1;">
                                <h3 style="margin: 0; font-size: 1.25rem;">
                                    <a href="{app_url}" target="_blank" rel="noopener noreferrer" style="color: #1e3a8a; text-decoration: none; font-weight: 700;">
                                        #{idx} — {card_title} 🔗
                                    </a>
                                    {prio_badge}
                                </h3>
                                <div style="color: #475569; font-weight: 600; font-size: 1.0rem; margin-top: 6px;">
                                    🏢 <strong>{card_company}</strong> &nbsp;•&nbsp; 📍 {card_location} &nbsp;•&nbsp; 💰 ${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}
                                </div>
                            </div>
                            <span class="{badge_class}">{score:.0f}% Fit</span>
                        </div>
                        <div style="margin: 0.75rem 0;">
                            <span class="clearance-badge" style="background: {'#fee2e2; color: #991b1b' if clr_is_fail else '#f1f5f9; color: #1e3a8a'};">
                                🛡️ Clearance: {clr_req} {'(⛔ INELIGIBLE)' if clr_is_fail else ''}
                            </span>
                            &nbsp;<span style="font-size: 0.85rem; color: #166534; font-weight: 700;">🎖️ Veteran-Friendly Employer</span>
                            &nbsp;<span style="font-size: 0.85rem; color: #64748b;">(Category: {job.get('category', 'General')})</span>
                        </div>
                        <p style="color: #334155; font-size: 0.95rem; margin-bottom: 0.75rem;">
                            {card_desc}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # KEY FACTORS SCORECARD & PROJECTED SELF-IMPROVEMENT
                    with st.expander(f"📊 Key Match Factors & Projected Success Breakdown"):
                        col_fc1, col_fc2 = st.columns(2)
                        with col_fc1:
                            st.markdown("#### 📋 Individual Key Match Factors")
                            # Role
                            r_st = "✅" if factors.get("role", {}).get("status") == "pass" else "⚠️"
                            st.markdown(f"**🎯 Role & Track Alignment:** {r_st} {factors.get('role', {}).get('detail', 'N/A')}")
                            # Clearance
                            c_st = "✅" if factors.get("clearance", {}).get("status") == "pass" else "⛔"
                            st.markdown(f"**🛡️ Security Clearance:** {c_st} {factors.get('clearance', {}).get('detail', 'N/A')}")
                            # Skills
                            s_st = "✅" if factors.get("skills", {}).get("status") == "pass" else "⚠️"
                            st.markdown(f"**💼 Skills Coverage:** {s_st} {factors.get('skills', {}).get('detail', 'N/A')}")
                            # Salary
                            sal_st = "✅" if factors.get("salary", {}).get("status") == "pass" else "⚠️"
                            st.markdown(f"**💰 Compensation Fit:** {sal_st} {factors.get('salary', {}).get('detail', 'N/A')}")
                            # Location
                            l_st = "✅" if factors.get("location", {}).get("status") == "pass" else "⚠️"
                            st.markdown(f"**📍 Location & Travel Distance:** {l_st} {factors.get('location', {}).get('detail', 'N/A')}")

                        with col_fc2:
                            st.markdown("#### 📈 Projected Success with Self-Improvement")
                            cur_sc = score
                            proj_sc = factors.get("projected_score", min(98.0, cur_sc + 15.0))
                            sc_gain = factors.get("score_delta", round(proj_sc - cur_sc, 1))
                            sal_gain = factors.get("projected_salary_gain", 15000)

                            st.markdown(f"""
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem;">
                                <div style="font-size: 0.95rem; margin-bottom: 6px;">
                                    <strong>Current Compatibility:</strong> <span style="font-weight: 700; color: #0b2545;">{cur_sc:.0f}%</span>
                                </div>
                                <div style="font-size: 0.95rem; margin-bottom: 6px;">
                                    <strong>Projected Match with Skill Bridge:</strong> <span style="font-weight: 700; color: #166534;">{proj_sc:.0f}% (+{sc_gain:.0f}% Uplift)</span>
                                </div>
                                <div style="font-size: 0.95rem; margin-bottom: 6px;">
                                    <strong>Estimated Annual Compensation Gain:</strong> <span style="font-weight: 700; color: #0284c7;">+${sal_gain:,.0f}/yr</span>
                                </div>
                                <div style="font-size: 0.85rem; color: #64748b; margin-top: 8px;">
                                    <em>Tip: Check Tab 2 for 100% free veteran funding links for these certifications.</em>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Missing skills tags
                            miss_list = factors.get("skills", {}).get("missing", [])
                            if miss_list:
                                st.markdown(f"**Missing Target Competencies:** {', '.join([s.title() for s in miss_list[:4]])}")

                    col_btn1, col_btn2 = st.columns([2, 1])
                    with col_btn1:
                        with st.expander(f"🔍 Why this matches your military background"):
                            for r in job.get("match_reasons", []):
                                st.markdown(f"• **{r}**")
                    with col_btn2:
                        st.link_button(
                            "🚀 Apply Direct on Official Portal",
                            app_url,
                            help=f"Opens direct application page for {job['title']} at {job['company']} in a new tab",
                            use_container_width=True
                        )
                        if st.button(f"🦅 Request 7 Eagle Recruiter Intro", key=f"intro_req_{idx}", use_container_width=True):
                            get_platform_metrics(increment_intro=True)
                            st.success(f"✅ Recruiter Intro requested for **{job['title']}** at **{job['company']}**! A 7 Eagle Group coordinator will contact {profile['email']}.")

            # Download / Export Section
            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                export_cols = ['title', 'company', 'location_display', 'salary_min', 'salary_max', 'match_score', 'application_url']
                export_data = []
                for j in top_matches:
                    export_data.append({
                        'title': j.get('title'),
                        'company': j.get('company'),
                        'location_display': j.get('location_display'),
                        'salary_min': j.get('salary_min'),
                        'salary_max': j.get('salary_max'),
                        'match_score': j.get('match_score'),
                        'application_url': j.get('application_url') or j.get('url')
                    })
                export_df = pd.DataFrame(export_data)
                st.download_button(
                    label="📥 Download Top Job Matches (CSV)",
                    data=export_df.to_csv(index=False),
                    file_name=f"veteran_matches_{profile['name'].replace(' ', '_').lower()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_exp2:
                summary_txt = f"""FOR YOUR SERVICE - VETERAN TRANSITION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Partner: 7 Eagle Group (https://7eagle.com)

VETERAN PROFILE:
- Name: {profile['name']}
- Branch: {profile['branch']}
- Rank: {profile['rank']}
- MOS / Specialty: {profile['mos']}
- Clearance: {profile['clearance']}
- Target Track: {profile.get('target_track', 'Operations')}
- Target Location: {profile['target_city']}, {profile['target_state']}
- Target Salary: ${profile['salary_min']:,.0f} - ${profile['salary_max']:,.0f}

TOP MATCHING CAREER OPPORTUNITIES:
"""
                for i, j in enumerate(top_matches, 1):
                    j_url = j.get('application_url') or j.get('url')
                    summary_txt += f"{i}. {j['title']} at {j['company']} | Score: {j['match_score']:.0f}% | Salary: ${j['salary_min']:,.0f}-${j['salary_max']:,.0f} | Apply: {j_url}\n"

                st.download_button(
                    label="📄 Download Full Veteran Transition Summary (TXT)",
                    data=summary_txt,
                    file_name=f"veteran_transition_summary_{profile['name'].replace(' ', '_').lower()}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        # TAB 2: CAREER READINESS & SKILL GAP OPTIMIZER
        with tab_readiness:
            st.markdown(f"### 🚀 Career Readiness & Skill Gap Analysis: **{readiness.get('target_track', '')}**")
            st.markdown(
                "Our Siamese Neural Network analyzes the vector distance between your profile and top job requirements "
                "in your chosen career track. Here is your personalized action plan to maximize your competitiveness and compensation."
            )

            # Uplift Metrics Banner
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                st.metric("Current Match Compatibility", f"{readiness.get('current_score', 0):.0f}%")
            with r_col2:
                gain = readiness.get('score_gain', 0)
                st.metric("Projected Compatibility", f"{readiness.get('projected_score', 0):.0f}%", delta=f"+{gain:.0f}% Uplift")
            with r_col3:
                sal_gain = readiness.get('est_salary_uplift', 15000)
                st.metric("Projected Salary Growth", f"+${sal_gain:,.0f}/yr", delta="Target Potential")

            st.markdown("---")

            # INTERACTIVE WHAT-IF CAREER & CREDENTIAL SIMULATOR
            st.markdown("### 🔮 Interactive 'What-If' Career & Credential Simulator")
            st.markdown("Select credentials you are interested in acquiring to see your live projected match score, interview probability, and salary growth:")

            sim_certs = readiness.get("recommended_certs", [])
            selected_sim_certs = []

            if sim_certs:
                sim_cols = st.columns(len(sim_certs))
                for idx, c in enumerate(sim_certs):
                    with sim_cols[idx]:
                        if st.checkbox(f"Add {c['name'].split('(')[0].strip()}", key=f"sim_chk_{idx}"):
                            selected_sim_certs.append(c)

                # Simulator Real-Time Math
                base_score = readiness.get('current_score', 70.0)
                sim_score_boost = sum([c['score_uplift'] for c in selected_sim_certs])
                simulated_score = min(99.0, base_score + sim_score_boost)
                sim_salary_boost = sum([c['salary_uplift'] for c in selected_sim_certs])

                prob_label = "Very High (90%+)" if simulated_score >= 88 else ("High (75-89%)" if simulated_score >= 75 else "Moderate (60-74%)")
                prob_color = "#16a34a" if simulated_score >= 88 else ("#0284c7" if simulated_score >= 75 else "#d97706")

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0b2545 0%, #134074 100%); color: white; border-radius: 10px; padding: 1.25rem; margin: 1rem 0; box-shadow: 0 4px 12px rgba(11,37,69,0.15);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div>
                            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Simulated Profile Fit</div>
                            <div style="font-size: 2rem; font-weight: 800; color: #f8fafc;">{simulated_score:.0f}% Compatibility</div>
                        </div>
                        <div>
                            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Interview Probability</div>
                            <div style="font-size: 1.4rem; font-weight: 700; color: {prob_color};">{prob_label}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Projected Value Uplift</div>
                            <div style="font-size: 1.6rem; font-weight: 800; color: #d4af37;">+${sim_salary_boost:,.0f}/yr</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # 1. Skill Gap Analysis
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("#### ✅ Skills You Already Have")
                if readiness.get("matching_skills"):
                    match_html = "".join([f"<span class='ops-skill-chip'>✓ {s.upper()}</span> " for s in readiness["matching_skills"]])
                    st.markdown(match_html, unsafe_allow_html=True)
                else:
                    st.info("Upload your full resume to highlight all matching strengths.")

            with col_g2:
                st.markdown("#### 🎯 Target Skills to Add / Highlight")
                if readiness.get("missing_skills"):
                    miss_html = "".join([f"<span class='skill-chip'>+ {s.upper()}</span> " for s in readiness["missing_skills"]])
                    st.markdown(miss_html, unsafe_allow_html=True)
                else:
                    st.success("Great job! You have strong coverage of the core skills for this track.")

            st.markdown("---")

            # 2. Recommended High-Impact Certifications (Free for Veterans)
            st.markdown("#### 🏆 Recommended High-Impact Certifications & Free Funding")
            st.markdown(
                "These industry-recognized credentials bridge the gap for your target role. "
                "**All certifications below have free funding programs for military veterans!**"
            )

            for cert in readiness.get("recommended_certs", []):
                with st.container():
                    st.markdown(f"""
                    <div style="background: white; border: 1px solid #cbd5e1; border-left: 6px solid #d4af37; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: #0b1d3a;">🎓 {cert['name']}</h4>
                            <span style="background: #fef3c7; color: #92400e; font-weight: 700; font-size: 0.85rem; padding: 0.2rem 0.6rem; border-radius: 12px;">
                                +{cert['score_uplift']}% Match • +${cert['salary_uplift']:,}/yr
                            </span>
                        </div>
                        <p style="margin: 0.5rem 0; color: #475569; font-size: 0.9rem;">
                            <strong>Provider:</strong> {cert['provider']}<br>
                            <strong>🎖️ Free Veteran Access:</strong> {cert['free_for_veterans']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button(f"🛡️ Access Free Training / Exam Voucher ({cert['name']})", cert["url"], use_container_width=True)

            st.markdown("---")

            # 3. Military-to-Civilian Resume Phrasing Recommendations
            st.markdown("#### 📝 Military-to-Civilian Resume Translation Tips")
            st.markdown("Civilian hiring managers and ATS algorithms respond best to civilianized terminology:")

            for military_phrase, civilian_phrase in readiness.get("resume_tips", []):
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.error(f"❌ **Military Phrasing:** {military_phrase}")
                with col_p2:
                    st.success(f"✅ **Civilian Recommendation:** {civilian_phrase}")


# ============================================================================
# VIEW 2: MOS CAREER CROSSWALK EXPLORER
# ============================================================================

elif nav_selection == "🗺️ MOS Career Crosswalk Explorer":
    st.markdown("## 🗺️ Military Occupational Specialty (MOS) Career Crosswalk")
    st.markdown(
        "Explore how military specialties across the **Army, Navy, Air Force, Marine Corps, Coast Guard, and Space Force** "
        "translate directly into high-paying civilian career paths, transferable skills, and compensation benchmarks."
    )

    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        branch_filter = st.selectbox("Filter by Service Branch:", ["All Branches", "Army", "Navy", "Air Force", "Marine Corps", "Coast Guard", "Space Force"])
    with col_s2:
        search_query = st.text_input("🔍 Search MOS Code, Title, or Civilian Keyword:", placeholder="e.g., 11B, 18F, 88M, 92Y, 68W, IT, Cyber, Logistics, Police...")

    filtered_mos = {}
    for code, data in MOS_DATABASE.items():
        if branch_filter != "All Branches" and data["branch"] != branch_filter:
            continue
        if search_query:
            q = search_query.lower()
            in_code = q in code.lower()
            in_title = q in data["title"].lower()
            in_civ = any(q in c.lower() for c in data["civilian_titles"])
            in_skills = any(q in s.lower() for s in data["transferable_skills"])
            in_cat = q in data.get("category", "").lower()
            if not (in_code or in_title or in_civ or in_skills or in_cat):
                continue
        filtered_mos[code] = data

    st.markdown(f"**Showing {len(filtered_mos)} military specialties:**")

    for code, data in filtered_mos.items():
        with st.expander(f"**{code} — {data['title']}** ({data['branch']})"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**🎖️ Category:** {data.get('category', 'General')}")
                st.markdown(f"**🛡️ Typical Clearance:** `{data.get('typical_clearance', 'Secret')}`")
                st.markdown("**🎯 Primary Civilian Job Titles:**")
                for ct in data["civilian_titles"]:
                    st.markdown(f"• **{ct}**")
            with col2:
                st.markdown("**💼 Core Transferable Strengths:**")
                for ts in data["transferable_skills"]:
                    st.markdown(f"• {ts.title()}")
                if data.get("tech_skills"):
                    st.markdown("**💻 Technical Tools & Systems:**")
                    st.markdown(", ".join([f"`{t}`" for t in data["tech_skills"]]))


# ============================================================================
# VIEW 3: 7 EAGLE GROUP & VETERAN RESOURCES
# ============================================================================

elif nav_selection == "🦅 7 Eagle Group & Resources":
    st.markdown("## 🦅 7 Eagle Group — Dedicated to Veteran Careers")
    st.markdown(
        "**7 Eagle Group** connects transitioning military service members, veterans, and military spouses with premier "
        "employers nationwide. We believe military experience is America's greatest leadership and technical talent pool."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🎖️ Why Partner With 7 Eagle Group?
        * **1-on-1 Veteran Mentorship:** Work with seasoned veteran recruiters who speak your language.
        * **Direct Hiring Pipeline:** Direct introductions to hiring managers at defense contractors, Fortune 500 tech companies, and high-growth startups.
        * **Zero Cost to Veterans:** 100% free placement services for all military personnel and spouses.
        * **Clearance Sponsorship & Placement:** Dedicated placement for Secret, Top Secret, and TS/SCI clearance holders.
        """)
        st.link_button("🌐 Visit 7 Eagle Group Official Portal", "https://7eagle.com", use_container_width=True)

    with col2:
        st.markdown("""
        ### 📚 Free Veteran Upskilling & Transition Resources
        * **AWS SkillBuilder for Veterans:** Free cloud certification training for service members.
        * **Onward to Opportunity (O2O):** Free career training & professional certification prep (PMP, Security+, CISSP, AWS).
        * **VetSec:** Non-profit cybersecurity community offering free training and mentoring for veterans.
        * **USAJOBS Veterans Preference:** Direct hiring authorities (VRA, VEOA, 30%+ Disabled Veteran).
        """)
        st.link_button("🛡️ Access Veteran Certification Programs", "https://ivmf.syracuse.edu/programs/career-training/", use_container_width=True)


# ============================================================================
# FOOTER & BACKEND DATA ENGINEERING TECH STACK SUMMARY
# ============================================================================

st.markdown("---")

with st.expander("⚙️ Backend Architecture & Data Engineering Tech Stack Summary"):
    st.markdown(r"""
    ### 🏗️ Backend System Architecture & Data Engineering Stack
    **Lead Architect & Developer:** **Free Hall** — *Cloud Engineer • DevOps Analyst • Data Architect* (18Z / 18F, US Army Special Forces, Ret.)

    * **Medallion Lakehouse Architecture (Databricks & Delta Lake):**
        * **Bronze Layer (`workspace.fys_bronze.job_postings`):** Automated multi-source ingestion pipeline aggregating active opportunities across USAJOBS, Adzuna, and JSearch REST APIs with schema enforcement and deduplication.
        * **Silver Layer (`workspace.fys_silver.veteran_profiles`):** PII-anonymized candidate ingestion, O*NET taxonomy skill normalization, and military MOS/AFSC/Rating crosswalk translation.
        * **Gold Layer (`workspace.fys_gold.job_embeddings`):** 384-dimensional dense semantic vector representations powered by `sentence-transformers/all-MiniLM-L6-v2`.
    * **AI Neural Matching & Career Readiness Engine:**
        * **PyTorch Siamese Twin Tower Neural Network:** Deep learning model evaluating candidate-to-job semantic compatibility via cosine similarity.
        * **Delta Vector Skill Gap Attribution ($\Delta = J_{\\text{target}} - V_{\\text{candidate}}$):** Isolates high-residual missing competencies and maps them to high-impact certifications with 100% free veteran funding.
    * **Zero-Cost & Serverless Cloud Hybrid:**
        * Runs on Databricks Serverless Compute in production; automatically falls back to 100% free local CPU execution for offline / zero-cost operation.
    * **Streamlit Responsive Frontend:**
        * Mobile-first, cross-platform UI optimized for iOS Safari, Android Chrome, macOS, and Windows.
    """)

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem 0; line-height: 1.6;">
    <img src="https://flagcdn.com/w40/us.png" width="22" height="14" alt="US Flag" style="vertical-align: middle; border-radius: 2px; margin-right: 6px; display: inline-block;">
    <strong>For Your Service</strong> | AI-Powered Veteran Job Matching Platform<br>
    Proudly Partnered with <strong>7 Eagle Group</strong> | Free & Open Source for Veterans<br>
    Lead Architect & Developer: <strong>Free Hall</strong> (Cloud Engineer • DevOps Analyst • Data Architect | 18Z / 18F, US Army Special Forces, Ret.)<br>
    <em>🎖️ Serving Those Who Served 🎖️</em>
</div>
""", unsafe_allow_html=True)
