#!/usr/bin/env python3
"""
File: sandbox/recon_app.py
Description: Isolated Sandbox Talent Reconnaissance Engine & Dynamic Targeting
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Sandbox Isolation Protocol (Veteran Foot-in-the-Door Priority)
"""

import pandas as pd
import urllib.parse
import os
import re

# --- LOCAL SANDBOX DATA LOADER ---
def load_sandbox_ledger() -> pd.DataFrame:
    data_path = os.path.join(os.path.dirname(__file__), "mock_data.csv")
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return pd.DataFrame({
        "name": ["William Free Hall", "Jane Doe", "John Smith"],
        "company": ["GE Aerospace", "GE Aerospace", "Lockheed Martin"],
        "title": ["Sr AI Data Engineer", "Cloud Engineer", "Data Architect"],
        "location": ["Greenville, SC", "Greenville, SC", "Fort Worth, TX"],
        "branch": ["US Army", "US Air Force", "US Navy"],
        "clearance": ["TS/SCI", "Secret", "Secret"],
        "is_veteran": [True, True, True],
        "skills": ["PySpark, Delta Lake", "Python, AWS", "SQL, Spark"],
        "profile_url": ["#", "#", "#"]
    })


def generate_sandbox_boolean_query(company: str = "GE Aerospace", role: str = "", location: str = "Greenville, SC", branch: str = "") -> str:
    """Constructs tailored Boolean X-Ray query prioritizing GE Aerospace Greenville veterans."""
    clauses = ["site:linkedin.com/in"]
    
    if company:
        if "ge" in company.lower() or "general electric" in company.lower():
            clauses.append('("GE Aerospace" OR "General Electric" OR "GE Aviation")')
        else:
            clauses.append(f'"{company}"')
            
    if location:
        if "greenville" in location.lower():
            clauses.append('("Greenville" OR "Spartanburg" OR "South Carolina" OR "SC")')
        elif "remote" in location.lower():
            clauses.append('("Remote" OR "United States")')
        else:
            clauses.append(f'"{location}"')
            
    if branch and branch != "All Veterans":
        clauses.append(f'("{branch}" OR "Veteran" OR "Military")')
    else:
        clauses.append('("Veteran" OR "Army" OR "Navy" OR "Air Force" OR "Marine" OR "Special Forces" OR "DoD" OR "Clearance")')
        
    if "ge" in (company or "").lower() and "greenville" in (location or "").lower():
        # High-yield role spectrum for GE Aerospace Greenville veterans
        clauses.append('("Engineer" OR "Data" OR "Manager" OR "Leader" OR "Architect" OR "Software" OR "AI")')
    elif role:
        clauses.append(f'("{role}" OR "Data Engineer" OR "AI Engineer" OR "Engineer")')
        
    return " ".join(clauses)


def generate_shared_patch_template(name: str = "[Name]", company: str = "GE Aerospace", location: str = "Greenville") -> str:
    """High-impact veteran connection message leading with shared service bond."""
    loc_clean = location.split(",")[0].strip() if "," in location else location
    return f"Hi {name}, saw you're making waves over at {company} in {loc_clean}. As a retired Special Forces Green Beret / Tech Lead transitioning into senior data engineering in the local area, I'm looking to connect with fellow veterans in the tech stack there. Would love to swap notes for 10 minutes if you're open to it."


def run_streamlit_app():
    import streamlit as st
    
    st.set_page_config(
        page_title="Recon Sandbox | Veteran Foot-in-the-Door",
        page_icon="🛡️",
        layout="wide"
    )

    st.title("🛡️ Sandbox: Talent Reconnaissance Engine")
    st.markdown("### 🎖️ Veteran Foot-in-the-Door Priority: GE Aerospace (Greenville, SC)")

    # --- QUICK MISSION PRESETS ---
    st.markdown("##### ⚡ Quick Mission Profiles")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("✈️ GE Aerospace Greenville (Veteran Insiders)", use_container_width=True):
            st.session_state["sb_comp"] = "GE Aerospace"
            st.session_state["sb_role"] = "Sr AI Data Engineer"
            st.session_state["sb_loc"] = "Greenville, SC"
            st.rerun()
    with q2:
        if st.button("🚀 Lockheed Martin Greenville (Defense AI)", use_container_width=True):
            st.session_state["sb_comp"] = "Lockheed Martin"
            st.session_state["sb_role"] = "AI Data Architect"
            st.session_state["sb_loc"] = "Greenville, SC"
            st.rerun()
    with q3:
        if st.button("☁️ AWS Defense (Remote Veteran Solutions)", use_container_width=True):
            st.session_state["sb_comp"] = "Amazon Web Services"
            st.session_state["sb_role"] = "Solutions Architect"
            st.session_state["sb_loc"] = "Remote"
            st.rerun()

    # --- INPUT CONTROL PANEL ---
    st.markdown("#### 🎯 Tactical Search Parameters")
    with st.form(key="sandbox_recon_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            target_company = st.text_input("Target Company", value=st.session_state.get("sb_comp", "GE Aerospace"), placeholder="e.g., GE Aerospace, Lockheed Martin")
        with col2:
            target_position = st.text_input("Target Position / Role", value=st.session_state.get("sb_role", "Sr AI Data Engineer"), placeholder="e.g., Sr AI Data Engineer, Cloud Architect")
        with col3:
            target_location = st.text_input("Target Location", value=st.session_state.get("sb_loc", "Greenville, SC"), placeholder="e.g., Greenville, SC, Remote")
            
        f_subcol1, f_subcol2 = st.columns(2)
        with f_subcol1:
            branch_filter = st.selectbox(
                "Branch Filter",
                ["All Veterans", "US Army (Special Forces / 18F / 18Z)", "US Air Force", "US Navy", "US Marine Corps", "US Space Force"],
                index=0
            )
        with f_subcol2:
            veteran_only = st.checkbox("Mandatory Veteran Filter (Foot-in-the-Door Priority)", value=True)
            
        submit_button = st.form_submit_button(label="⚡ Execute Veteran Recon Search", use_container_width=True)

    # --- VETERAN-FIRST PRIORITY FILTER LOGIC ---
    df = load_sandbox_ledger()
    
    # Base mandatory filter: Must be a veteran for this specific mission
    mask = pd.Series([True] * len(df))
    if veteran_only:
        mask &= (df['is_veteran'] == True)

    if target_company:
        if "ge" in target_company.lower():
            mask &= df['company'].str.contains("GE|General Electric", case=False, na=False)
        else:
            mask &= df['company'].str.contains(re.escape(target_company), case=False, na=False)

    if target_position:
        role_tokens = [t for t in target_position.replace("Sr", "").replace("Senior", "").strip().split() if len(t) > 2]
        if role_tokens:
            pat = "|".join([re.escape(t) for t in role_tokens])
            mask &= df['title'].str.contains(pat, case=False, na=False)

    if target_location:
        clean_loc = target_location.split(",")[0].strip()
        mask &= df['location'].str.contains(re.escape(clean_loc), case=False, na=False)

    if branch_filter and branch_filter != "All Veterans":
        clean_branch = branch_filter.split("(")[0].strip()
        mask &= df['branch'].str.contains(re.escape(clean_branch), case=False, na=False)

    results = df[mask].copy()

    # --- TABS: RESULTS & STRATEGY ---
    tab1, tab2, tab3 = st.tabs([
        "🎖️ Veteran Foot-in-the-Door Targets",
        "📡 Tailored Boolean X-Ray Launcher",
        "💬 The Shared Patch (Connection Message)"
    ])

    with tab1:
        st.subheader(f"Veteran Foot-in-the-Door Targets Found ({len(results)})")
        if not results.empty:
            st.dataframe(results[['name', 'company', 'title', 'location', 'branch', 'clearance', 'skills']], use_container_width=True)
        else:
            st.warning("[!] No veteran targets found matching these exact coordinates. Widen search radius or use the Live Boolean X-Ray tab to scan external profiles.")

    with tab2:
        st.subheader("📡 Tailored Boolean X-Ray for GE Aerospace Veterans")
        st.markdown("Copy and paste this exact search string into your browser or click below to launch instant search across public indexed LinkedIn profiles:")
        
        b_query = generate_sandbox_boolean_query(target_company, target_position, target_location, branch_filter)
        st.code(b_query, language="text")

        encoded_q = urllib.parse.quote_plus(b_query)
        g_url = f"https://www.google.com/search?q={encoded_q}"
        d_url = f"https://duckduckgo.com/?q={encoded_q}"
        li_url = f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote_plus(f'{target_company} {target_location} Veteran {target_position}')}&origin=GLOBAL_SEARCH_HEADER"

        b1, b2, b3 = st.columns(3)
        with b1:
            st.link_button("🚀 Launch Google X-Ray Search", g_url, use_container_width=True)
        with b2:
            st.link_button("🦆 Launch DuckDuckGo X-Ray", d_url, use_container_width=True)
        with b3:
            st.link_button("🔗 Direct LinkedIn Search", li_url, use_container_width=True)

    with tab3:
        st.subheader("💬 Veteran-to-Veteran Connection Note (The Shared Patch)")
        st.markdown("When connecting with a fellow veteran at GE Aerospace, lead with the shared service bond before pivoting to engineering:")
        
        target_name = st.text_input("Target Veteran's First Name", value="[Name]")
        patch_note = generate_shared_patch_template(name=target_name, company=target_company, location=target_location)
        
        st.text_area("Connection Request Note (< 300 chars, ready to paste into LinkedIn)", value=patch_note, height=120)
        
        st.download_button(
            label="📥 Download Connection Note",
            data=patch_note,
            file_name="ge_veteran_connection_note.txt",
            mime="text/plain"
        )

    st.markdown("""
    ---
    > 🎯 **Gunslinger Lore: The Shared Patch**  
    > *In the field, a unit patch or tab isn't just fabric—it's a blood-bought trust protocol. When reaching out to a fellow veteran inside GE Aerospace, you don't start with corporate elevator pitches. You flash the patch, establish the shared perimeter, and let the brotherhood open the breach.*
    """)

if __name__ == "__main__":
    run_streamlit_app()
