# ============================================================================
# For Your Service - Veteran Intake & Job Matching Portal 🇺🇸
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

# Import local MOS data and sample engine
try:
    from mos_data import MOS_DATABASE, lookup_mos, get_all_mos_choices
    from sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILE, load_cached_scraped_jobs
except ImportError:
    from app.mos_data import MOS_DATABASE, lookup_mos, get_all_mos_choices
    from app.sample_data import SAMPLE_JOBS, DEMO_VETERAN_PROFILE, load_cached_scraped_jobs

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
    page_title="For Your Service - Veteran Intake & Career Matching",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Patriotic CSS (Navy, Crimson, Gold, Clean White)
st.markdown("""
<style>
    /* Primary Colors: Deep Military Navy (#0B2545), Crimson (#C81D25), Gold (#D4AF37) */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0b1d3a 0%, #1e3a8a 50%, #13315c 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(11, 29, 58, 0.2);
        margin-bottom: 1.5rem;
        border-bottom: 4px solid #c81d25;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #e2e8f0;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    .hero-badge {
        display: inline-block;
        background: #d4af37;
        color: #0b1d3a;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        margin-top: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Branch Cards */
    .branch-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Match Score Badges */
    .match-badge-high {
        background-color: #15803d;
        color: white;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }
    .match-badge-med {
        background-color: #d97706;
        color: white;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        display: inline-block;
    }
    
    /* Job Card */
    .job-card {
        background: white;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #1e3a8a;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Skill Chip */
    .skill-chip {
        display: inline-block;
        background: #e0e7ff;
        color: #1e3a8a;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
    }
    .mil-skill-chip {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
    }
    
    /* Clearance Badge */
    .clearance-badge {
        background: #1e293b;
        color: #f8fafc;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid #475569;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1e3a8a;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0b1d3a;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS FOR RESUME EXTRACTION & SKILLS
# ============================================================================

def extract_text_from_file(uploaded_file) -> str:
    """Extract raw text from uploaded PDF, DOCX, or TXT file (100% free/local)"""
    if uploaded_file is None:
        return ""
    
    filename = uploaded_file.name.lower()
    
    try:
        # PDF Extraction
        if filename.endswith(".pdf"):
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
            except Exception:
                import pypdf
                reader = pypdf.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
                
        # DOCX Extraction
        elif filename.endswith(".docx"):
            import docx
            doc = docx.Document(uploaded_file)
            return "\n".join([p.text for p in doc.paragraphs])
            
        # Plain text
        elif filename.endswith(".txt"):
            return uploaded_file.getvalue().decode("utf-8", errors="ignore")
            
        else:
            return uploaded_file.getvalue().decode("utf-8", errors="ignore")
            
    except Exception as e:
        st.warning(f"⚠️ Notice reading file: {str(e)}. You can also paste your resume text directly.")
        return ""


def parse_veteran_skills(resume_text: str, mos_code: str = "") -> Dict:
    """Extract technical and military leadership skills from resume text & MOS"""
    text_lower = resume_text.lower()
    
    # Technical skills taxonomy
    tech_keywords = [
        "aws", "azure", "gcp", "kubernetes", "docker", "terraform", "python", "java",
        "javascript", "sql", "bash", "powershell", "jenkins", "github", "gitlab",
        "ci/cd", "devops", "linux", "windows", "ansible", "cisco", "active directory",
        "palantir", "databricks", "spark", "pyspark", "delta lake", "networking",
        "cybersecurity", "siem", "splunk", "wireshark", "penetration testing", "security+",
        "cissp", "vmware", "tableau", "power bi", "excel", "satcom", "cryptography"
    ]
    
    # Military & Leadership competencies
    leadership_keywords = [
        "executive briefings", "cross-functional leadership", "mission planning",
        "risk management", "opsec", "link analysis", "operations management",
        "crisis decision making", "inter-agency coordination", "team sergeant",
        "squad leader", "platoon sergeant", "command", "process optimization",
        "standard operating procedures", "personnel accountability", "logistics"
    ]
    
    detected_tech = [skill for skill in tech_keywords if skill in text_lower]
    detected_leadership = [lead for lead in leadership_keywords if lead in text_lower]
    
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
    total_years = max([int(y) for y in years_matches], default=5)
    
    if total_years >= 10:
        seniority = "Senior / Executive Lead"
    elif total_years >= 5:
        seniority = "Mid-to-Senior Professional"
    else:
        seniority = "Associate / Entry Specialist"
        
    return {
        "technical_skills": list(set(detected_tech)),
        "leadership_skills": list(set(detected_leadership)),
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
    Calculate semantic match score (0-100) and generate 'Why You Match' reasons.
    """
    score = 0.0
    reasons = []
    
    job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
    user_skills = set(extracted_skills.get("technical_skills", []))
    leadership_skills = set(extracted_skills.get("leadership_skills", []))
    
    # 1. Technical Skills Match (Max 35 pts)
    job_req_skills = [s.lower() for s in job.get("skills", [])]
    if job_req_skills:
        matched_req = [s for s in job_req_skills if s in user_skills or s in job_text]
        skill_pct = min(1.0, len(matched_req) / max(1, len(job_req_skills)))
        tech_score = skill_pct * 35
        score += tech_score
        if matched_req:
            reasons.append(f"Technical Match: {', '.join([s.title() for s in matched_req[:4]])}")
    else:
        matched_in_text = [s for s in user_skills if s in job_text]
        tech_score = min(35.0, len(matched_in_text) * 7.0)
        score += tech_score
        if matched_in_text:
            reasons.append(f"Skills Found: {', '.join([s.title() for s in matched_in_text[:4]])}")

    # 2. MOS & Military Experience Crosswalk (Max 25 pts)
    mos_info = lookup_mos(veteran_profile.get("mos", ""))
    if mos_info:
        mos_civilian_titles = [t.lower() for t in mos_info.get("civilian_titles", [])]
        job_title_lower = job.get("title", "").lower()
        
        # Check if job title matches civilian title mappings
        if any(ct in job_title_lower or job_title_lower in ct for ct in mos_civilian_titles):
            score += 25
            reasons.append(f"Direct MOS Crosswalk: Aligns with {mos_info['title']}")
        elif any(ts in job_text for ts in mos_info.get("transferable_skills", [])):
            score += 18
            reasons.append(f"Military Experience Match: Transferable {mos_info.get('branch')} skill fit")
        else:
            score += 10
            
    # 3. Security Clearance Alignment (Max 15 pts)
    job_clearance = str(job.get("clearance_required", "None")).strip()
    vet_clearance = str(veteran_profile.get("clearance", "None")).strip()
    
    clearance_hierarchy = {
        "None": 0,
        "Public Trust": 1,
        "Secret": 2,
        "Top Secret": 3,
        "Top Secret / SCI": 4,
        "TS / SCI with CI Poly": 5,
        "TS / SCI with Full Scope Poly": 6
    }
    
    job_clr_level = clearance_hierarchy.get(job_clearance, 0)
    vet_clr_level = clearance_hierarchy.get(vet_clearance, 0)
    
    if job_clr_level > 0 and vet_clr_level >= job_clr_level:
        score += 15
        reasons.append(f"Clearance Advantage: Active {vet_clearance} satisfies requirement")
    elif job_clr_level == 0:
        score += 10
    else:
        score += 0
        
    # 4. Salary Alignment (Max 15 pts)
    job_sal_min = float(job.get("salary_min", 0) or 0)
    job_sal_max = float(job.get("salary_max", 0) or 0)
    vet_sal_min = float(veteran_profile.get("salary_min", 0) or 0)
    vet_sal_max = float(veteran_profile.get("salary_max", 0) or 0)
    
    if job_sal_max >= vet_sal_min and job_sal_min <= vet_sal_max:
        score += 15
        reasons.append("Compensation: Perfectly meets desired salary target")
    elif job_sal_max >= vet_sal_min * 0.9:
        score += 10
    else:
        score += 5
        
    # 5. Location & Remote Flexibility (Max 10 pts)
    vet_state = veteran_profile.get("target_state", "").upper()
    job_state = job.get("state", "").upper()
    
    if "remote" in job.get("location_display", "").lower() or veteran_profile.get("remote_ok", False):
        score += 10
        reasons.append("Location: Remote / Flexible location match")
    elif vet_state and (vet_state == job_state):
        score += 10
        reasons.append(f"Location: Local match in {vet_state}")
    else:
        score += 5
        
    final_score = min(100.0, max(25.0, score))
    return round(final_score, 1), reasons


# ============================================================================
# SIDEBAR: NAVIGATION, DEMO PROFILE & PLATFORM STATUS
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
    st.markdown("### 🚀 Fast Demo Profile")
    st.markdown("Test the entire pipeline in **1 click** with Lead Developer Free Hall's profile (18F / Solutions Architect):")
    
    if st.button("🇺🇸 Load Demo Profile (18F)", use_container_width=True):
        st.session_state["demo_loaded"] = True
        st.session_state["form_name"] = DEMO_VETERAN_PROFILE["name"]
        st.session_state["form_email"] = DEMO_VETERAN_PROFILE["email"]
        st.session_state["form_phone"] = DEMO_VETERAN_PROFILE["phone"]
        st.session_state["form_branch"] = DEMO_VETERAN_PROFILE["branch"]
        st.session_state["form_rank"] = DEMO_VETERAN_PROFILE["rank"]
        st.session_state["form_mos"] = DEMO_VETERAN_PROFILE["mos"]
        st.session_state["form_clearance"] = DEMO_VETERAN_PROFILE["clearance"]
        st.session_state["form_status"] = DEMO_VETERAN_PROFILE["service_status"]
        st.session_state["form_city"] = DEMO_VETERAN_PROFILE["target_city"]
        st.session_state["form_state"] = DEMO_VETERAN_PROFILE["target_state"]
        st.session_state["form_sal_min"] = DEMO_VETERAN_PROFILE["salary_min"]
        st.session_state["form_sal_max"] = DEMO_VETERAN_PROFILE["salary_max"]
        st.session_state["form_resume"] = DEMO_VETERAN_PROFILE["resume_text"]
        st.toast("✅ Demo Veteran Profile Loaded!", icon="🎖️")
        
    st.markdown("---")
    st.markdown("### ⚙️ Compute & Lakehouse Mode")
    if SPARK_AVAILABLE:
        st.success("🟢 Databricks Serverless Active\n\nConnected to Unity Catalog")
    else:
        st.info("🔵 Zero-Cost Local / Free Tier\n\nRunning in local mode with cached job datasets (100% Free)")
        
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.8rem; color: #64748b; text-align: center;'>
            <strong>For Your Service</strong><br>
            Designed & Built by Veterans for Veterans<br>
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
    <div class="hero-title">🇺🇸 FOR YOUR SERVICE</div>
    <div class="hero-subtitle">AI-Powered Veteran Career Intake & Military-to-Civilian Job Matching Platform</div>
    <div class="hero-badge">🎖️ Partner: 7 Eagle Group | Serving Those Who Served</div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# VIEW 1: VETERAN INTAKE & JOB MATCHING
# ============================================================================

if nav_selection == "📋 Veteran Intake & Match":

    # Quick summary metrics banner
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='branch-card'><strong>🪖 U.S. Army</strong><br><small>Infantry, Special Forces, Cyber, Intel</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='branch-card'><strong>⚓ U.S. Navy</strong><br><small>IT, Cryptologic, Engineering, Medical</small></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='branch-card'><strong>✈️ U.S. Air Force</strong><br><small>Cyber Warfare, Space, Operations</small></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='branch-card'><strong>🦅 U.S. Marines & CG</strong><br><small>Data Systems, Leadership, Logistics</small></div>", unsafe_allow_html=True)

    st.markdown("")

    # Form Container
    with st.form("veteran_intake_form", clear_on_submit=False):
        
        # --------------------------------------------------------------------
        # STEP 1: MILITARY SERVICE & BACKGROUND
        # --------------------------------------------------------------------
        st.markdown("### 🎖️ Step 1: Military Service & Specialty")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            branches = ["Army", "Navy", "Air Force", "Marine Corps", "Coast Guard", "Space Force"]
            branch_default_idx = 0
            if "form_branch" in st.session_state and st.session_state["form_branch"] in branches:
                branch_default_idx = branches.index(st.session_state["form_branch"])
                
            service_branch = st.selectbox(
                "Branch of Service *",
                branches,
                index=branch_default_idx,
                help="Select the military branch you served in"
            )
            
        with col_m2:
            ranks = [
                "E-1 to E-4 (Junior Enlisted)",
                "E-5 to E-6 (NCO / Team Leader)",
                "E-7 to E-9 (Senior NCO / Master Sgt / First Sgt / SGM)",
                "W-1 to W-5 (Warrant Officer)",
                "O-1 to O-3 (Company Grade Officer)",
                "O-4 to O-6 (Field Grade Officer)",
                "O-7+ (General / Flag Officer)"
            ]
            rank_default_idx = 2
            if "form_rank" in st.session_state:
                for idx, r in enumerate(ranks):
                    if "E-7" in r or "E-8" in r:
                        rank_default_idx = idx
                        break
            pay_grade = st.selectbox("Rank / Pay Grade Category *", ranks, index=rank_default_idx)
            
        with col_m3:
            service_statuses = [
                "Veteran (Separated / Discharged)",
                "Veteran (Retired)",
                "Active Duty (Transitioning / ETS soon)",
                "National Guard / Reserve"
            ]
            status_default_idx = 1 if "form_status" in st.session_state and "Retired" in st.session_state["form_status"] else 0
            service_status = st.selectbox("Current Service Status *", service_statuses, index=status_default_idx)

        # MOS / AFSC / Rating Code Input
        col_mos1, col_mos2 = st.columns([1, 2])
        with col_mos1:
            mos_default = st.session_state.get("form_mos", "18F")
            mos_code = st.text_input(
                "MOS / AFSC / Rating Code *",
                value=mos_default,
                placeholder="e.g., 18Z, 18F, 25B, IT, 1D7X1, 0651",
                help="Enter your primary Military Specialty code"
            ).strip().upper()
            
        with col_mos2:
            clearances = [
                "None / Public Trust",
                "Secret",
                "Top Secret",
                "Top Secret / SCI",
                "TS / SCI with CI Poly",
                "TS / SCI with Full Scope Poly"
            ]
            clr_default_idx = 3 if "form_clearance" in st.session_state and "Top Secret / SCI" in st.session_state["form_clearance"] else 1
            clearance_level = st.selectbox("Active Security Clearance *", clearances, index=clr_default_idx)

        # Dynamic MOS Crosswalk Preview Box
        if mos_code:
            mos_preview = lookup_mos(mos_code)
            if mos_preview:
                st.info(
                    f"**🎖️ MOS Crosswalk Identified:** `{mos_code}` — **{mos_preview['title']}** ({mos_preview['branch']})\n\n"
                    f"• **Civilian Career Paths:** {', '.join(mos_preview['civilian_titles'])}\n\n"
                    f"• **Transferable Strengths:** {', '.join(mos_preview['transferable_skills'][:6])}"
                )

        st.markdown("---")

        # --------------------------------------------------------------------
        # STEP 2: CONTACT & CIVILIAN PREFERENCES
        # --------------------------------------------------------------------
        st.markdown("### 📋 Step 2: Contact Info & Civilian Career Goals")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            name_val = st.session_state.get("form_name", "")
            full_name = st.text_input("Full Name *", value=name_val, placeholder="William Free Hall")
        with col_c2:
            email_val = st.session_state.get("form_email", "")
            email_addr = st.text_input("Email Address *", value=email_val, placeholder="veteran@example.com")
        with col_c3:
            phone_val = st.session_state.get("form_phone", "")
            phone_num = st.text_input("Phone Number", value=phone_val, placeholder="(910) 584-3843")

        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            city_val = st.session_state.get("form_city", "Greenville")
            target_city = st.text_input("Target City *", value=city_val, placeholder="Greenville")
        with col_l2:
            state_val = st.session_state.get("form_state", "SC")
            target_state = st.text_input("Target State (2-letter code) *", value=state_val, max_chars=2, placeholder="SC").upper()
        with col_l3:
            remote_pref = st.checkbox("Open to Remote / Hybrid Roles", value=True)
            relocate_pref = st.checkbox("Willing to Relocate for Right Opportunity", value=True)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            sal_min_val = st.session_state.get("form_sal_min", 90000)
            salary_min = st.slider(
                "Minimum Desired Annual Salary ($)",
                min_value=40000,
                max_value=220000,
                value=int(sal_min_val),
                step=5000,
                format="$%d"
            )
        with col_s2:
            sal_max_val = st.session_state.get("form_sal_max", 160000)
            salary_max = st.slider(
                "Target / Maximum Annual Salary ($)",
                min_value=50000,
                max_value=250000,
                value=int(sal_max_val),
                step=5000,
                format="$%d"
            )

        st.markdown("---")

        # --------------------------------------------------------------------
        # STEP 3: RESUME & EXPERIENCE INGESTION
        # --------------------------------------------------------------------
        st.markdown("### 📄 Step 3: Resume & Military Experience Ingestion")
        st.markdown(
            "*Upload your resume in PDF, DOCX, or TXT format, or paste your resume text below. "
            "Our 100% free parser will extract your technical skills, leadership competencies, and military accomplishments.*"
        )

        uploaded_file = st.file_uploader("Upload Resume File (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
        
        # Determine resume text from upload or session
        resume_default_text = st.session_state.get("form_resume", "")
        if uploaded_file is not None:
            extracted_file_text = extract_text_from_file(uploaded_file)
            if extracted_file_text:
                resume_default_text = extracted_file_text
                st.success(f"✅ Successfully extracted text from `{uploaded_file.name}` ({len(extracted_file_text)} characters)")

        resume_text = st.text_area(
            "Resume Text / Work History & Certifications *",
            value=resume_default_text,
            height=250,
            placeholder="Paste your complete resume or military summary here...\n\nInclude military awards, specialties, technical tools (AWS, Python, Kubernetes, Cisco), and leadership achievements."
        )

        st.markdown("")
        submit_btn = st.form_submit_button("🚀 Find Matching Opportunities & Register Profile", use_container_width=True)

    # ------------------------------------------------------------------------
    # FORM SUBMISSION & MATCHING EXECUTION
    # ------------------------------------------------------------------------
    if submit_btn:
        if not full_name or not email_addr or not target_city or not target_state or not resume_text:
            st.error("🚨 Please fill out all required fields (*) before submitting.")
        elif len(target_state) != 2:
            st.error("🚨 Target State must be a 2-letter state abbreviation (e.g., SC, NC, FL, TX).")
        elif salary_min >= salary_max:
            st.error("🚨 Minimum desired salary must be less than the target maximum salary.")
        elif len(resume_text.strip()) < 80:
            st.error("🚨 Resume text is too short. Please provide a complete resume or work summary (at least 80 characters).")
        else:
            with st.spinner("🔄 Parsing veteran profile, extracting military-to-civilian skills, and computing matches..."):
                veteran_id = str(uuid.uuid4())
                
                # 1. Parse Skills
                extracted = parse_veteran_skills(resume_text, mos_code)
                
                # 2. Build Profile Object
                veteran_profile = {
                    "veteran_id": veteran_id,
                    "name": full_name,
                    "email": email_addr,
                    "phone": phone_num,
                    "branch": service_branch,
                    "rank": pay_grade,
                    "mos": mos_code,
                    "clearance": clearance_level,
                    "service_status": service_status,
                    "target_city": target_city,
                    "target_state": target_state,
                    "remote_ok": remote_pref,
                    "relocation": relocate_pref,
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "total_years": extracted["total_years"],
                    "seniority": extracted["seniority"],
                    "technical_skills": extracted["technical_skills"],
                    "leadership_skills": extracted["leadership_skills"]
                }
                
                # 3. Store in Unity Catalog if Spark is available
                if SPARK_AVAILABLE and spark:
                    try:
                        profile_df = spark.createDataFrame([{
                            "veteran_id": veteran_id,
                            "name": full_name,
                            "email": email_addr,
                            "branch": service_branch,
                            "rank": pay_grade,
                            "mos_code": mos_code,
                            "clearance": clearance_level,
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
                    except Exception as e:
                        pass  # Gracefully continue to local matching

                # 4. Load Job Postings
                all_jobs = load_cached_scraped_jobs()
                
                # 5. Compute Matches
                matches = []
                for job in all_jobs:
                    score, reasons = calculate_veteran_match_score(job, veteran_profile, extracted)
                    # Filter: Match score threshold or location
                    matches.append({
                        **job,
                        "match_score": score,
                        "match_reasons": reasons
                    })
                
                # Sort by score descending
                matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)
                
                # Save to session state for display
                st.session_state["current_matches"] = matches
                st.session_state["current_profile"] = veteran_profile
                st.session_state["current_extracted"] = extracted

    # ------------------------------------------------------------------------
    # MATCH RESULTS DISPLAY
    # ------------------------------------------------------------------------
    if "current_matches" in st.session_state and st.session_state["current_matches"]:
        matches = st.session_state["current_matches"]
        profile = st.session_state["current_profile"]
        extracted = st.session_state["current_extracted"]
        
        st.markdown("---")
        st.markdown(f"## 🎯 Career Match Results for **{profile['name']}**")
        
        # Profile Summary Header
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        with summary_col1:
            st.metric("Top Match Score", f"{matches[0]['match_score']:.0f}%")
        with summary_col2:
            st.metric("Total Jobs Evaluated", f"{len(matches)}")
        with summary_col3:
            st.metric("Experience Level", f"{profile['seniority'].split('/')[0].strip()}")
        with summary_col4:
            st.metric("Active Clearance", f"{profile['clearance'].split('/')[0].strip()}")
            
        # Extracted Skills Tag Cloud
        st.markdown("#### 🔍 Extracted Candidate Skills & Military Competencies")
        skills_html = ""
        for s in extracted["technical_skills"][:12]:
            skills_html += f"<span class='skill-chip'>💻 {s.upper()}</span>"
        for l in extracted["leadership_skills"][:6]:
            skills_html += f"<span class='mil-skill-chip'>🎖️ {l.title()}</span>"
        if extracted.get("mos_skills"):
            for m in extracted["mos_skills"][:4]:
                skills_html += f"<span class='mil-skill-chip'>🪖 {m.title()}</span>"
        st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown("")

        # Match Cards
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
                        &nbsp;<span style="font-size: 0.85rem; color: #64748b;">(Source: {job.get('source', 'Adzuna')})</span>
                    </div>
                    <p style="color: #334155; font-size: 0.95rem; margin-bottom: 0.75rem;">
                        {job.get('description', '')[:300]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Match reasons & action buttons
                col_btn1, col_btn2 = st.columns([2, 1])
                with col_btn1:
                    with st.expander(f"🔍 Why this matches your military background"):
                        for r in job.get("match_reasons", []):
                            st.markdown(f"• **{r}**")
                with col_btn2:
                    st.link_button("🔗 Apply Directly", job.get("url", "https://adzuna.com"), use_container_width=True)
                    if st.button(f"🦅 Request 7 Eagle Intro", key=f"intro_{idx}", use_container_width=True):
                        st.toast(f"✅ Recruiter Intro requested for {job['title']} at {job['company']}! A 7 Eagle Group coordinator will reach out to {profile['email']}.", icon="🦅")

        # Download / Export Section
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            export_df = pd.DataFrame(top_matches)[['title', 'company', 'location_display', 'salary_min', 'salary_max', 'match_score', 'url']]
            st.download_button(
                label="📥 Download Top Job Matches (CSV)",
                data=export_df.to_csv(index=False),
                file_name=f"veteran_matches_{profile['name'].replace(' ', '_').lower()}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_d2:
            summary_txt = f"""FOR YOUR SERVICE - VETERAN TRANSITION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Partner: 7 Eagle Group

VETERAN PROFILE:
- Name: {profile['name']}
- Branch: {profile['branch']}
- Rank: {profile['rank']}
- MOS: {profile['mos']}
- Clearance: {profile['clearance']}
- Target Location: {profile['target_city']}, {profile['target_state']}
- Target Salary: ${profile['salary_min']:,.0f} - ${profile['salary_max']:,.0f}

TOP MATCHING OPPORTUNITIES:
"""
            for i, j in enumerate(top_matches, 1):
                summary_txt += f"{i}. {j['title']} at {j['company']} | Score: {j['match_score']:.0f}% | Salary: ${j['salary_min']:,.0f}-${j['salary_max']:,.0f} | URL: {j['url']}\n"
                
            st.download_button(
                label="📄 Download Veteran Transition Summary (TXT)",
                data=summary_txt,
                file_name=f"veteran_transition_summary_{profile['name'].replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )


# ============================================================================
# VIEW 2: MOS CAREER CROSSWALK EXPLORER
# ============================================================================

elif nav_selection == "🗺️ MOS Career Crosswalk Explorer":
    st.markdown("## 🗺️ Military Occupational Specialty (MOS) Career Crosswalk")
    st.markdown(
        "Explore how military specialties across the **Army, Navy, Air Force, Marine Corps, Space Force, and Coast Guard** "
        "translate directly into civilian job titles, transferable skills, and compensation benchmarks."
    )
    
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        branch_filter = st.selectbox("Filter by Service Branch:", ["All Branches", "Army", "Navy", "Air Force", "Marine Corps", "Coast Guard", "Space Force"])
    with col_s2:
        search_query = st.text_input("🔍 Search MOS Code, Title, or Civilian Keyword:", placeholder="e.g., 18Z, Cyber, Intelligence, Logistics, 25B, Cloud")
        
    filtered_mos = {}
    for code, data in MOS_DATABASE.items():
        # Branch match
        if branch_filter != "All Branches" and data["branch"] != branch_filter:
            continue
        # Search match
        if search_query:
            q = search_query.lower()
            in_code = q in code.lower()
            in_title = q in data["title"].lower()
            in_civ = any(q in c.lower() for c in data["civilian_titles"])
            in_skills = any(q in s.lower() for s in data["transferable_skills"])
            if not (in_code or in_title or in_civ or in_skills):
                continue
        filtered_mos[code] = data

    st.markdown(f"**Found {len(filtered_mos)} matching military specialties:**")
    
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
                st.markdown("**💼 Core Transferable Skills:**")
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
    🇺🇸 <strong>For Your Service</strong> | AI-Powered Veteran Job Matching Platform<br>
    Proudly Partnered with <strong>7 Eagle Group</strong> | Free & Open Source for Veterans<br>
    Lead Developer: <strong>Free Hall</strong> (18Z / 18F, US Army Special Forces, Ret.)<br>
    <em>🎖️ Serving Those Who Served 🎖️</em>
</div>
""", unsafe_allow_html=True)