#!/usr/bin/env python3
"""
File: app/linkedin_finder_app.py
Description: Standalone Interactive LinkedIn Veteran & Aerospace AI Talent Finder
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Gunslinger Clean-Core
"""

import streamlit as st
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
    page_title="LinkedIn Veteran Talent Finder | Aerospace AI",
    page_icon="🎯",
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
        padding: 15px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎯 LinkedIn Veteran & Aerospace AI Talent Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Target Vector: Sr AI Data Engineer • GE Aerospace • Greenville, SC Corridor</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Search Parameters")
    
    company = st.selectbox("Target Company", DEFAULT_COMPANIES, index=0)
    role = st.selectbox("Target Role", DEFAULT_ROLES, index=0)
    location = st.selectbox("Target Location", DEFAULT_LOCATIONS, index=0)
    
    branch_filter = st.selectbox(
        "Military Background Filter",
        ["All Veterans", "US Army (Special Forces / 18F / 18Z)", "US Air Force / Space Force", "US Navy", "US Marine Corps", "TS/SCI & Secret Clearance"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 👤 Operator Profile")
    sender_name = st.text_input("Your Name", value="Free Hall")
    sender_branch = st.text_input("Your Background", value="US Army Special Forces (18F / 18Z, Ret.)")
    sender_title = st.text_input("Your Target Title", value="Senior AI Data Engineer & Lakehouse Architect")

# Initialize finder
branch_arg = None if branch_filter == "All Veterans" else branch_filter
finder = LinkedInVeteranFinder(
    company=company,
    role=role,
    location=location,
    branch_filter=branch_arg
)

boolean_query = finder.generate_boolean_query()
google_url = finder.generate_google_search_url()
ddg_url = finder.generate_duckduckgo_url()
li_url = finder.generate_direct_linkedin_search_url()

# -----------------------------------------------------------------------------
# TABS INTERFACE
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🔍 1-Click X-Ray & Search Launcher",
    "💬 Warm Outreach & Intro Generator",
    "🎯 Curated GE Aerospace Target Vectors"
])

# -----------------------------------------------------------------------------
# TAB 1: X-RAY SEARCH LAUNCHER
# -----------------------------------------------------------------------------
with tab1:
    st.markdown("### 📡 Formulated Boolean X-Ray Query")
    st.markdown(
        "Google & Search Engine X-Ray queries bypass LinkedIn login restrictions by searching public, indexed LinkedIn profiles matching your exact criteria:"
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
    st.markdown("### 💡 How X-Ray Searching Works")
    st.info(
        """
        * **`site:linkedin.com/in`**: Restricts the search specifically to individual personal profiles on LinkedIn.
        * **Company Filtering**: Combines *"GE Aerospace"* and *"General Electric"* to capture both brand transitions.
        * **Role & Military Operators**: Intersects AI/Data Engineering terms with military service and clearance markers to isolate veteran engineers.
        """
    )

# -----------------------------------------------------------------------------
# TAB 2: WARM OUTREACH GENERATOR
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("### 💬 Veteran-to-Veteran Peer Networking & Executive Outreach")
    
    outreach_type = st.radio(
        "Select Outreach Strategy",
        ["Peer-to-Peer Veteran Networking (Engineer-to-Engineer)", "Executive / Hiring Manager Direct Outreach"],
        horizontal=True
    )
    
    if outreach_type == "Peer-to-Peer Veteran Networking (Engineer-to-Engineer)":
        target_name = st.text_input("Target Peer's First Name", value="Alex")
        message = finder.generate_peer_outreach_message(
            peer_name=target_name,
            sender_name=sender_name,
            sender_branch=sender_branch,
            target_role=role
        )
    else:
        manager_name = st.text_input("Target Manager's Name", value="Hiring Team Lead")
        message = finder.generate_hiring_manager_outreach_message(
            manager_name=manager_name,
            sender_name=sender_name,
            sender_title=sender_title,
            target_role=role
        )
        
    st.text_area("Generated Outreach Message (Ready to Copy)", value=message, height=260)
    
    st.download_button(
        label="📥 Download Message as Text File",
        data=message,
        file_name="ge_aerospace_outreach_message.txt",
        mime="text/plain"
    )

# -----------------------------------------------------------------------------
# TAB 3: CURATED TARGETS
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("### 🎯 Curated GE Aerospace Target Search Vectors")
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
