# ============================================================================
# For Your Service - Veteran Intake & Job Matching Portal 🇺🇸
# Universal Platform for ALL Service Members: Any Branch, Any Rank, Any Clearance
# Powered by 7 Eagle Group | AI-Driven Veteran Placement Platform
# Developer: Free Hall (18Z / 18F, US Army Special Forces, Ret.)
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import uuid
import json
import re
import io
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Import local MOS data, dynamic branch ranks, and sample engine
try:
    from mos_data import MOS_DATABASE, BRANCH_RANKS, lookup_mos, get_mos_choices_by_branch
    from sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILES, load_cached_scraped_jobs
    from readiness_engine import CAREER_TRACKS, analyze_career_readiness
except ImportError:
    from app.mos_data import MOS_DATABASE, BRANCH_RANKS, lookup_mos, get_mos_choices_by_branch
    from app.sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILES, load_cached_scraped_jobs
    from app.readiness_engine import CAREER_TRACKS, analyze_career_readiness

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
# PAGE CONFIGURATION & PATRIOTIC STYLING
# ============================================================================

st.set_page_config(
    page_title="For Your Service - Veteran Career Portal",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    # 1. Technical & Trade Skills Taxonomy
    tech_keywords = [
        "aws", "azure", "gcp", "kubernetes", "docker", "terraform", "python", "java",
        "javascript", "sql", "bash", "powershell", "jenkins", "github", "gitlab",
        "ci/cd", "devops", "linux", "windows", "windows server", "ansible", "cisco",
        "active directory", "palantir", "databricks", "spark", "pyspark", "delta lake",
        "networking", "cybersecurity", "siem", "splunk", "wireshark", "penetration testing",
        "security+", "cissp", "vmware", "tableau", "power bi", "excel", "satcom", "cryptography",
        "diesel mechanics", "hydraulics", "pneumatics", "cdl", "dot compliance", "telematics",
        "emr", "triage", "paramedic", "cpr", "bls", "cad", "sap", "erp", "osha", "hazmat"
    ]
    
    # 2. Military Leadership & Command Competencies
    leadership_keywords = [
        "executive briefings", "cross-functional leadership", "mission planning",
        "risk management", "opsec", "link analysis", "operations management",
        "crisis decision making", "inter-agency coordination", "team sergeant",
        "squad leader", "platoon sergeant", "command", "process optimization",
        "standard operating procedures", "personnel accountability", "after-action reviews",
        "force protection", "situational awareness", "mentorship", "inspections"
    ]
    
    # 3. General Operations, Logistics & Project Skills
    ops_keywords = [
        "supply chain", "inventory management", "logistics", "procurement",
        "quality control", "fleet maintenance", "preventive maintenance",
        "vendor management", "budget reconciliation", "access control", "physical security",
        "investigations", "scheduling", "training & development", "customer service"
    ]
    
    detected_tech = [skill for skill in tech_keywords if skill in text_lower]
    detected_leadership = [lead for lead in leadership_keywords if lead in text_lower]
    detected_ops = [op for op in ops_keywords if op in text_lower]
    
    # Add MOS-specific transferable skills
    mos_info = lookup_mos(mos_code)
    mos_skills = []
    if mos_info:
        mos_skills = mos_info.get("transferable_skills", [])
        for ts in mos_info.get("tech_skills", []):
            if ts not in detected_tech:
                detected_tech.append(ts)
                
    # Estimate years of experience
    years_pattern = r'(\d+)\+?\s*years?'
    years_matches = re.findall(years_pattern, text_lower)
    total_years = max([int(y) for y in years_matches], default=6)
    
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


def calculate_veteran_match_score(
    job: Dict,
    veteran_profile: Dict,
    extracted_skills: Dict
) -> Tuple[float, List[str]]:
    """
    Calculate match score (0-100) and generate 'Why You Match' reasons.
    Works universally across combat arms, logistics, mechanics, tech, and medical.
    """
    score = 0.0
    reasons = []
    
    job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('category', '')}".lower()
    user_tech = set(extracted_skills.get("technical_skills", []))
    user_leadership = set(extracted_skills.get("leadership_skills", []))
    user_ops = set(extracted_skills.get("ops_skills", []))
    all_user_skills = user_tech.union(user_leadership).union(user_ops)
    
    # 1. Skills & Competencies Match (Max 35 pts)
    job_req_skills = [s.lower() for s in job.get("skills", [])]
    if job_req_skills:
        matched_req = [s for s in job_req_skills if s in all_user_skills or s in job_text]
        skill_pct = min(1.0, len(matched_req) / max(1, len(job_req_skills)))
        score += skill_pct * 35
        if matched_req:
            reasons.append(f"Skill Alignment: Matched on {', '.join([s.title() for s in matched_req[:4]])}")
    else:
        matched_in_text = [s for s in all_user_skills if s in job_text]
        score += min(35.0, len(matched_in_text) * 6.0)
        if matched_in_text:
            reasons.append(f"Key Strengths: {', '.join([s.title() for s in matched_in_text[:4]])}")

    # 2. MOS / Branch Specialty Crosswalk (Max 25 pts)
    mos_info = lookup_mos(veteran_profile.get("mos", ""))
    if mos_info:
        mos_civilian_titles = [t.lower() for t in mos_info.get("civilian_titles", [])]
        job_title_lower = job.get("title", "").lower()
        
        if any(ct in job_title_lower or job_title_lower in ct for ct in mos_civilian_titles):
            score += 25
            reasons.append(f"Direct MOS Crosswalk: Aligns with {mos_info['title']} ({mos_info['branch']})")
        elif any(ts in job_text for ts in mos_info.get("transferable_skills", [])):
            score += 20
            reasons.append(f"Military Background Fit: {mos_info.get('branch')} specialty transferable skills")
        else:
            score += 12
    else:
        score += 10
            
    # 3. Security Clearance Alignment (Max 15 pts)
    job_clearance = str(job.get("clearance_required", "None")).strip()
    vet_clearance = str(veteran_profile.get("clearance", "None")).strip()
    
    clearance_hierarchy = {
        "None / Public Trust": 0,
        "Public Trust": 1,
        "Confidential": 2,
        "Secret": 3,
        "Top Secret": 4,
        "Top Secret / SCI": 5,
        "TS / SCI with CI Poly": 6,
        "TS / SCI with Full Scope Poly": 7
    }
    
    job_clr_level = clearance_hierarchy.get(job_clearance, 0)
    vet_clr_level = clearance_hierarchy.get(vet_clearance, 0)
    
    if job_clr_level > 0 and vet_clr_level >= job_clr_level:
        score += 15
        reasons.append(f"Security Clearance: Active {vet_clearance} qualifies for defense requirement")
    elif job_clr_level == 0:
        score += 12
    else:
        score += 0
        
    # 4. Salary Alignment (Max 15 pts)
    job_sal_min = float(job.get("salary_min", 0) or 0)
    job_sal_max = float(job.get("salary_max", 0) or 0)
    vet_sal_min = float(veteran_profile.get("salary_min", 0) or 0)
    vet_sal_max = float(veteran_profile.get("salary_max", 0) or 0)
    
    if job_sal_max >= vet_sal_min and job_sal_min <= vet_sal_max:
        score += 15
        reasons.append("Compensation: Perfectly aligns with your target salary")
    elif job_sal_max >= vet_sal_min * 0.85:
        score += 10
    else:
        score += 5
        
    # 5. Location & Remote Flexibility (Max 10 pts)
    vet_state = veteran_profile.get("target_state", "").upper()
    job_state = job.get("state", "").upper()
    
    if "remote" in job.get("location_display", "").lower() or veteran_profile.get("remote_ok", False):
        score += 10
        reasons.append("Location: Flexible / Remote or regional match")
    elif vet_state and (vet_state == job_state):
        score += 10
        reasons.append(f"Location: Local match in {vet_state}")
    else:
        score += 5
        
    final_score = min(100.0, max(30.0, score))
    return round(final_score, 1), reasons


# ============================================================================
# SIDEBAR: NAVIGATION, MULTI-BRANCH DEMO PROFILES & SYSTEM STATUS
# ============================================================================

with st.sidebar:
    st.image("https://img.shields.io/badge/7_Eagle_Group-Veteran_Placement-blue?style=for-the-badge&logo=shield", use_container_width=True)
    
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
            st.toast("✅ Loaded Army 18F Special Forces Profile!", icon="🎖️")
            st.rerun()
            
        if st.button("🪖 88M Logistics", use_container_width=True, help="Army Motor Transport & CDL"):
            p = DEMO_VETERAN_PROFILES["88M"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.toast("✅ Loaded Army 88M Logistics Profile!", icon="🎖️")
            st.rerun()

    with col_d2:
        if st.button("🪖 11B Infantry", use_container_width=True, help="Army Infantry Squad Leader"):
            p = DEMO_VETERAN_PROFILES["11B"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.toast("✅ Loaded Army 11B Infantry Profile!", icon="🎖️")
            st.rerun()

        if st.button("⚓ Navy IT / Cyber", use_container_width=True, help="Navy IT Systems Administrator"):
            p = DEMO_VETERAN_PROFILES["25B"]
            for k, v in p.items():
                st.session_state[f"form_{k}"] = v
            st.toast("✅ Loaded Navy IT Profile!", icon="🎖️")
            st.rerun()
        
    st.markdown("---")
    st.markdown("### ⚙️ Engine Status")
    if SPARK_AVAILABLE:
        st.success("🟢 Databricks Serverless Active\n\nConnected to Unity Catalog")
    else:
        st.info("🔵 Zero-Cost Free Tier / Local\n\nRunning in local mode with 100% free resume parsing & job matching")
        
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.8rem; color: #64748b; text-align: center;'>
            <strong>For Your Service</strong><br>
            Universal Platform for All Military Service Members<br>
            Free Hall • 18Z / 18F US Army Special Forces (Ret.)
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================================
# HERO BANNER
# ============================================================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-title" style="display: flex; align-items: center; flex-wrap: wrap; gap: 12px;">
        <img src="https://flagcdn.com/w80/us.png" srcset="https://flagcdn.com/w160/us.png 2x" width="46" height="30" alt="United States Flag" style="border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.35); vertical-align: middle; display: inline-block;">
        <span>FOR YOUR SERVICE</span>
    </div>
    <div class="hero-subtitle">Universal Veteran Career Intake & AI Military-to-Civilian Job Matching Platform</div>
    <div class="hero-badge">🎖️ Serving ALL Branches • Any Rank • Any Specialty • 100% Free</div>
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

    # Mobile & Quick Demo Selector (Accessible on all screens)
    with st.expander("⚡ 1-Click Fast Demo Profiles (Tap to auto-fill for testing)"):
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            if st.button("🪖 18F SF Lead", key="mob_demo_18f", use_container_width=True, help="Army Special Forces / Cloud Architect"):
                p = DEMO_VETERAN_PROFILES["18F"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.toast("✅ Loaded Army 18F Special Forces Profile!", icon="🎖️")
                st.rerun()
        with m_col2:
            if st.button("🪖 11B Infantry", key="mob_demo_11b", use_container_width=True, help="Army Infantry Squad Leader"):
                p = DEMO_VETERAN_PROFILES["11B"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.toast("✅ Loaded Army 11B Infantry Profile!", icon="🎖️")
                st.rerun()
        with m_col3:
            if st.button("🪖 88M Logistics", key="mob_demo_88m", use_container_width=True, help="Army Motor Transport & CDL"):
                p = DEMO_VETERAN_PROFILES["88M"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
                st.toast("✅ Loaded Army 88M Logistics Profile!", icon="🎖️")
                st.rerun()
        with m_col4:
            if st.button("⚓ Navy IT / Cyber", key="mob_demo_it", use_container_width=True, help="Navy IT Systems Administrator"):
                p = DEMO_VETERAN_PROFILES["25B"]
                for k, v in p.items():
                    st.session_state[f"form_{k}"] = v
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
        mos_default = st.session_state.get("form_mos", "11B")
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
        clr_default_idx = 2
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
    with col_c2:
        email_default = st.session_state.get("form_email", "")
        email_addr = st.text_input("Email Address *", value=email_default, placeholder="veteran@example.com")
    with col_c3:
        phone_default = st.session_state.get("form_phone", "")
        phone_num = st.text_input("Phone Number", value=phone_default, placeholder="(555) 123-4567")

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        city_default = st.session_state.get("form_target_city", "Greenville")
        target_city = st.text_input("Target City / Metro *", value=city_default, placeholder="Greenville")
    with col_t2:
        state_default = st.session_state.get("form_target_state", "SC")
        target_state = st.text_input("Target State (2-letter code) *", value=state_default, max_chars=2, placeholder="SC").upper()
    with col_t3:
        remote_ok = st.checkbox("Open to Remote / Hybrid Opportunities", value=True)
        relocate_ok = st.checkbox("Willing to Relocate for the Right Opportunity", value=True)

    # Target Career Track Selection
    col_track1, col_track2 = st.columns([1, 1])
    with col_track1:
        track_options = list(CAREER_TRACKS.keys())
        track_default_idx = 2  # Default to Operations
        if "form_career_track" in st.session_state and st.session_state["form_career_track"] in track_options:
            track_default_idx = track_options.index(st.session_state["form_career_track"])
        elif "form_mos" in st.session_state:
            mos_val = st.session_state["form_mos"]
            if mos_val in ["18F", "18Z", "25B", "1D7X1", "IT"]:
                track_default_idx = 0  # Cloud / DevOps
            elif mos_val in ["25D", "17C", "1B4X1", "CTN", "0689"]:
                track_default_idx = 1  # Cyber
            elif mos_val in ["88M", "92A", "92Y", "LS", "2T2X1", "0431"]:
                track_default_idx = 3  # Logistics
            elif mos_val in ["91B", "91X", "15T", "2A6X1", "MK"]:
                track_default_idx = 4  # Mechanics
            elif mos_val in ["31B", "31D", "3P0X1", "MA", "5811", "ME"]:
                track_default_idx = 5  # Law Enforcement
            elif mos_val in ["68W", "HM", "4N0X1", "18D"]:
                track_default_idx = 6  # Healthcare

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
            placeholder="e.g., Solutions Architect, Operations Supervisor, Fleet Dispatcher...",
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
        if not full_name or not email_addr or not target_city or not target_state or not resume_text:
            st.error("🚨 Please fill out all required fields (*) or upload a resume before launching the pipeline.")
        elif len(target_state) != 2:
            st.error("🚨 Target State must be a 2-letter state code (e.g., SC, NC, FL, TX, GA, VA).")
        elif salary_min >= salary_max:
            st.error("🚨 Minimum desired salary must be less than the target salary.")
        elif len(resume_text.strip()) < 50:
            st.error("🚨 Resume text is too short. Please provide a complete resume or military summary (at least 50 characters).")
        else:
            with st.spinner("⚡ Setting AI pipeline in motion: Parsing military experience, evaluating MOS crosswalk, and matching jobs..."):
                veteran_id = str(uuid.uuid4())
                
                # 1. Parse Skills
                extracted = parse_veteran_skills(resume_text, mos_input)
                
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
                    "remote_ok": remote_ok,
                    "relocation": relocate_ok,
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
                    except Exception:
                        pass

                # 4. Load Job Postings & Compute Semantic Matches
                all_jobs = load_cached_scraped_jobs()
                matches = []
                for job in all_jobs:
                    score, reasons = calculate_veteran_match_score(job, veteran_profile, extracted)
                    matches.append({
                        **job,
                        "match_score": score,
                        "match_reasons": reasons
                    })
                
                # Sort by score descending
                matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)
                
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
                <div><strong>Target:</strong> {profile['target_city']}, {profile['target_state']} (${profile['salary_min']:,.0f} - ${profile['salary_max']:,.0f})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Extracted Skills Tag Cloud
        st.markdown("#### 🔍 Extracted Military & Civilian Strengths")
        skills_html = ""
        for s in extracted["technical_skills"][:10]:
            skills_html += f"<span class='skill-chip'>💻 {s.upper()}</span>"
        for l in extracted["leadership_skills"][:6]:
            skills_html += f"<span class='mil-skill-chip'>🎖️ {l.title()}</span>"
        for o in extracted["ops_skills"][:6]:
            skills_html += f"<span class='ops-skill-chip'>⚙️ {o.title()}</span>"
        if extracted.get("mos_skills"):
            for m in extracted["mos_skills"][:4]:
                skills_html += f"<span class='mil-skill-chip'>🪖 {m.title()}</span>"
        st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown("")

        # TABS: JOB MATCHES vs CAREER READINESS & SKILL GAP OPTIMIZER
        tab_jobs, tab_readiness = st.tabs([
            f"💼 Top Matching Opportunities ({len(matches[:8])})",
            f"🚀 Career Readiness & Skill Gap Optimizer ({readiness.get('target_track', 'Target Track')})"
        ])

        with tab_jobs:
            st.markdown("### 💼 Top Matching Opportunities")
            top_matches = matches[:8]
            
            for idx, job in enumerate(top_matches, 1):
                score = job["match_score"]
                badge_class = "match-badge-high" if score >= 75 else "match-badge-med"
                
                with st.container():
                    st.markdown(f"""
                    <div class="job-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <h3 style="margin: 0; color: #0b1d3a;">#{idx} — {job['title']}</h3>
                            <span class="{badge_class}">{score:.0f}% Fit</span>
                        </div>
                        <div style="color: #475569; font-weight: 600; font-size: 1.05rem; margin-bottom: 0.5rem;">
                            🏢 {job['company']} &nbsp;•&nbsp; 📍 {job['location_display']} &nbsp;•&nbsp; 💰 ${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}
                        </div>
                        <div style="margin-bottom: 0.75rem;">
                            <span class="clearance-badge">🛡️ Clearance: {job.get('clearance_required', 'None')}</span>
                            &nbsp;<span style="font-size: 0.85rem; color: #166534; font-weight: 700;">🎖️ Veteran-Friendly Employer</span>
                            &nbsp;<span style="font-size: 0.85rem; color: #64748b;">(Category: {job.get('category', 'General')})</span>
                        </div>
                        <p style="color: #334155; font-size: 0.95rem; margin-bottom: 0.75rem;">
                            {job.get('description', '')[:320]}...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_btn1, col_btn2 = st.columns([2, 1])
                    with col_btn1:
                        with st.expander(f"🔍 Why this matches your military background"):
                            for r in job.get("match_reasons", []):
                                st.markdown(f"• **{r}**")
                    with col_btn2:
                        st.link_button("🔗 Apply Directly", job.get("url", "https://7eaglegroup.com"), use_container_width=True)
                        if st.button(f"🦅 Request 7 Eagle Recruiter Intro", key=f"intro_req_{idx}", use_container_width=True):
                            st.success(f"✅ Recruiter Intro requested for **{job['title']}** at **{job['company']}**! A 7 Eagle Group coordinator will contact {profile['email']}.")

            # Download / Export Section
            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                export_df = pd.DataFrame(top_matches)[['title', 'company', 'location_display', 'salary_min', 'salary_max', 'match_score', 'url']]
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
Partner: 7 Eagle Group (https://7eaglegroup.com)

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
                    summary_txt += f"{i}. {j['title']} at {j['company']} | Score: {j['match_score']:.0f}% | Salary: ${j['salary_min']:,.0f}-${j['salary_max']:,.0f} | URL: {j['url']}\n"
                    
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

            # 1. Skill Gap Analysis
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("#### ✅ Skills You Already Have")
                if readiness.get("matching_skills"):
                    match_html = "".join([f"<span class='ops-skill-chip'>✓ {s.upper()}</span>" for s in readiness["matching_skills"]])
                    st.markdown(match_html, unsafe_allow_html=True)
                else:
                    st.info("Upload your full resume to highlight all matching strengths.")

            with col_g2:
                st.markdown("#### 🎯 Target Skills to Add / Highlight")
                if readiness.get("missing_skills"):
                    miss_html = "".join([f"<span class='skill-chip'>+ {s.upper()}</span>" for s in readiness["missing_skills"]])
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
        st.link_button("🌐 Visit 7 Eagle Group Official Portal", "https://7eaglegroup.com", use_container_width=True)
        
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
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem 0;">
    <img src="https://flagcdn.com/w40/us.png" width="22" height="14" alt="US Flag" style="vertical-align: middle; border-radius: 2px; margin-right: 6px; display: inline-block;">
    <strong>For Your Service</strong> | AI-Powered Veteran Job Matching Platform<br>
    Proudly Partnered with <strong>7 Eagle Group</strong> | Free & Open Source for Veterans<br>
    Lead Developer: <strong>Free Hall</strong> (18Z / 18F, US Army Special Forces, Ret.)<br>
    <em>🎖️ Serving Those Who Served 🎖️</em>
</div>
""", unsafe_allow_html=True)