#!/usr/bin/env python3
"""
File: app/linkedin_finder_app.py
Description: Dynamic Veteran Talent Reconnaissance Grid & LinkedIn Intel Engine
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Gunslinger Clean-Core
"""

import streamlit as st
import pandas as pd
import urllib.parse
import sys
import os

# Include project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.features.linkedin_veteran_finder import (
    LinkedInVeteranFinder,
    get_curated_ge_aerospace_targets,
    DEFAULT_COMPANIES,
    DEFAULT_ROLES,
    DEFAULT_LOCATIONS,
    MILITARY_KEYWORDS
)

st.set_page_config(
    page_title="Veteran Talent Recon Grid | Defense & AI Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 26px;
        color: #00FF66;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
    }
    .sub-header {
        font-family: 'Courier New', monospace;
        color: #00F0FF;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .query-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-left: 4px solid #00FF66;
        padding: 15px;
        border-radius: 6px;
        font-family: monospace;
        color: #00ffcc;
        font-size: 14px;
        word-break: break-all;
    }
    .target-card {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .badge-clearance {
        background-color: #7928CA;
        color: #FFFFFF;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-branch {
        background-color: #0070F3;
        color: #FFFFFF;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛡️ Veteran Talent Intelligence & Reconnaissance Grid</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Dynamic Personnel Recon, Lakehouse Matching & Live LinkedIn X-Ray Engine</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# QUICK PRESET SELECTORS
# -----------------------------------------------------------------------------
st.markdown("##### ⚡ Quick Coordinate Targets (Tap to Auto-Fill)")
p_col1, p_col2, p_col3, p_col4 = st.columns(4)
with p_col1:
    if st.button("✈️ GE Aerospace (Greenville)", key="preset_ge", use_container_width=True):
        st.session_state["dyn_comp"] = "GE Aerospace"
        st.session_state["dyn_role"] = "Sr AI Data Engineer"
        st.session_state["dyn_loc"] = "Greenville, SC"
        st.rerun()
with p_col2:
    if st.button("🚀 Lockheed Martin (Defense AI)", key="preset_lm", use_container_width=True):
        st.session_state["dyn_comp"] = "Lockheed Martin"
        st.session_state["dyn_role"] = "AI Data Architect"
        st.session_state["dyn_loc"] = "Greenville, SC"
        st.rerun()
with p_col3:
    if st.button("☁️ AWS Defense (Remote)", key="preset_aws", use_container_width=True):
        st.session_state["dyn_comp"] = "Amazon Web Services"
        st.session_state["dyn_role"] = "Solutions Architect"
        st.session_state["dyn_loc"] = "Remote"
        st.rerun()
with p_col4:
    if st.button("🛰️ Space Force / Cyber (DC)", key="preset_dc", use_container_width=True):
        st.session_state["dyn_comp"] = "Northrop Grumman"
        st.session_state["dyn_role"] = "DevSecOps Architect"
        st.session_state["dyn_loc"] = "Washington DC"
        st.rerun()

# -----------------------------------------------------------------------------
# DYNAMIC INPUT FORM
# -----------------------------------------------------------------------------
with st.form(key="recon_grid_form"):
    st.markdown("#### 🎯 Enter Operational Target Parameters")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        target_company = st.text_input(
            "Target Company / Organization",
            value=st.session_state.get("dyn_comp", "GE Aerospace"),
            placeholder="e.g., GE Aerospace, Lockheed Martin, SpaceX"
        )
    with f_col2:
        target_role = st.text_input(
            "Target Position / Role",
            value=st.session_state.get("dyn_role", "Sr AI Data Engineer"),
            placeholder="e.g., Sr AI Data Engineer, Cloud Architect, Systems Engineer"
        )
    with f_col3:
        target_location = st.text_input(
            "Target Location / Region",
            value=st.session_state.get("dyn_loc", "Greenville, SC"),
            placeholder="e.g., Greenville, SC, Huntsville, AL, Remote"
        )
        
    f_subcol1, f_subcol2 = st.columns(2)
    with f_subcol1:
        branch_filter = st.selectbox(
            "Military Background Filter",
            ["All Veterans", "US Army (Special Forces / 18F / 18Z)", "US Air Force / Space Force", "US Navy", "US Marine Corps", "TS/SCI & Secret Clearance"],
            index=0
        )
    with f_subcol2:
        veteran_only = st.checkbox("Enforce Veteran Status Only", value=True)
        
    submit_button = st.form_submit_button(label="⚡ Execute Reconnaissance & Generate X-Ray Vector", use_container_width=True)

# Initialize Dynamic Finder Instance
branch_arg = None if branch_filter == "All Veterans" else branch_filter
finder = LinkedInVeteranFinder(
    company=target_company,
    role=target_role,
    location=target_location,
    branch_filter=branch_arg
)

boolean_query = finder.generate_boolean_query()
google_url = finder.generate_google_search_url()
ddg_url = finder.generate_duckduckgo_url()
li_url = finder.generate_direct_linkedin_search_url()
matched_results = finder.search_talent_ledger(veteran_only=veteran_only)

# -----------------------------------------------------------------------------
# TABS INTERFACE
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🛰️ Personnel Recon Grid (Acquired Targets)",
    "📡 Live Web X-Ray & Search Launcher",
    "💬 Dynamic Outreach & Intro Generator",
    "🎯 Curated Defense & Aerospace Vectors"
])

# -----------------------------------------------------------------------------
# TAB 1: PERSONNEL RECON GRID
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f"### 🎯 Personnel Ledger Acquisition Results ({len(matched_results)} Matched Targets)")
    st.markdown(f"Filtering parameters: **Company:** `{target_company or 'Any'}` | **Role:** `{target_role or 'Any'}` | **Location:** `{target_location or 'Any'}`")
    
    if not matched_results.empty:
        for idx, row in matched_results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="target-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color:#00FF66; margin:0;">{row['name']}</h4>
                        <div>
                            <span class="badge-branch">{row['branch']}</span>
                            <span class="badge-clearance">{row['clearance']}</span>
                        </div>
                    </div>
                    <p style="margin: 6px 0 2px 0;"><strong>{row['title']}</strong> at <span style="color:#00F0FF;">{row['company']}</span> — <em>{row['location']}</em></p>
                    <p style="color:#A0AEC0; font-size:13px; margin-bottom:8px;"><strong>Core Skills:</strong> {row['skills']}</p>
                </div>
                """, unsafe_allow_html=True)
                
        # Dataframe View
        with st.expander("📊 View Raw Talent Ledger Data Table"):
            st.dataframe(matched_results[['name', 'company', 'title', 'location', 'branch', 'clearance', 'skills']], use_container_width=True)
    else:
        st.warning(f"⚠️ No internal ledger targets matched '{target_company}' / '{target_role}' / '{target_location}'. Launch the Live X-Ray Search below to scan external LinkedIn profiles!")

# -----------------------------------------------------------------------------
# TAB 2: LIVE WEB X-RAY LAUNCHER
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("### 📡 Formulated Boolean X-Ray Search Query")
    st.markdown(
        "This dynamic Boolean query searches all public Google/Bing indexed LinkedIn profiles matching your exact custom parameters + military service keywords:"
    )
    
    st.markdown(f'<div class="query-box">{boolean_query}</div>', unsafe_allow_html=True)
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button(
            "🚀 Launch Google X-Ray Search",
            google_url,
            help="Opens Google search targeting indexed LinkedIn profiles",
            use_container_width=True
        )
    with col2:
        st.link_button(
            "🦆 Launch DuckDuckGo X-Ray",
            ddg_url,
            help="Opens DuckDuckGo search targeting indexed LinkedIn profiles",
            use_container_width=True
        )
    with col3:
        st.link_button(
            "🔗 Direct LinkedIn People Search",
            li_url,
            help="Opens LinkedIn People Search directly with pre-filled filters",
            use_container_width=True
        )
        
    st.markdown("---")
    st.markdown("""
    > 🎯 **Gunslinger Lore: Dynamic Targeting Systems**  
    > *A true operator doesn't lock onto static coordinates—you adjust fire based on dynamic mission terrain. Whether the target is GE Aerospace in Greenville, Lockheed Martin in Fort Worth, or AWS GovCloud in DC, the targeting grid calculates the angle and delivers the connection.*
    """)

# -----------------------------------------------------------------------------
# TAB 3: DYNAMIC OUTREACH GENERATOR
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("### 💬 Dynamic Outreach & Intro Generator")
    
    outreach_type = st.radio(
        "Select Outreach Strategy",
        ["Peer-to-Peer Veteran Networking (Engineer-to-Engineer)", "Executive / Hiring Manager Direct Outreach"],
        horizontal=True
    )
    
    if outreach_type == "Peer-to-Peer Veteran Networking (Engineer-to-Engineer)":
        target_name = st.text_input("Target Peer's First Name", value="Alex")
        message = finder.generate_peer_outreach_message(
            peer_name=target_name,
            sender_name="Free Hall",
            sender_branch="US Army Special Forces (18F / 18Z, Ret.)",
            target_role=target_role
        )
    else:
        manager_name = st.text_input("Target Manager's Name", value="Hiring Team Lead")
        message = finder.generate_hiring_manager_outreach_message(
            manager_name=manager_name,
            sender_name="Free Hall",
            sender_title="Senior AI Data Engineer & Lakehouse Architect",
            target_role=target_role
        )
        
    st.text_area("Generated Outreach Message (Ready to Copy)", value=message, height=260)
    
    st.download_button(
        label=f"📥 Download Outreach Message for {target_company}",
        data=message,
        file_name=f"{target_company.lower().replace(' ', '_')}_outreach_message.txt",
        mime="text/plain"
    )

# -----------------------------------------------------------------------------
# TAB 4: CURATED DEFENSE VECTORS
# -----------------------------------------------------------------------------
with tab4:
    st.markdown("### 🎯 Curated Defense & Aerospace Target Vectors")
    targets = get_curated_ge_aerospace_targets()
    
    for t in targets:
        with st.container():
            st.markdown(f"""
            <div class="target-card">
                <h4 style="color:#00FF66; margin-top:0;">{t['role']} — {t['company']}</h4>
                <p><strong>Category:</strong> {t['category']} | <strong>Location:</strong> {t['location']}</p>
                <p><strong>Technical Focus:</strong> {t['focus_areas']}</p>
                <p style="font-family:monospace; color:#00f0ff; font-size:12px;">{t['boolean_sample']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            sample_encoded = urllib.parse.quote_plus(t['boolean_sample'])
            st.link_button(
                f"🔎 Launch Search for {t['role']}",
                f"https://www.google.com/search?q={sample_encoded}",
                use_container_width=False
            )
            st.markdown("")
