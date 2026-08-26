#!/usr/bin/env python3
"""
File: sandbox/recon_app.py
Description: Isolated Sandbox Talent Reconnaissance Engine & Dynamic Targeting
Author: Free Hall <whall4.wh@gmail.com>
Protocol: Sandbox Isolation Protocol
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


def generate_sandbox_boolean_query(company: str, role: str, location: str, branch: str = "") -> str:
    """Constructs dynamic Boolean X-Ray query."""
    clauses = ["site:linkedin.com/in"]
    
    if company:
        if "ge" in company.lower() or "general electric" in company.lower():
            clauses.append('("GE Aerospace" OR "General Electric" OR "GE Aviation")')
        else:
            clauses.append(f'"{company}"')
            
    if role:
        clauses.append(f'("{role}" OR "Data Engineer" OR "AI Engineer" OR "Engineer")')
        
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
        
    return " ".join(clauses)


def run_streamlit_app():
    import streamlit as st
    
    st.set_page_config(
        page_title="Recon Sandbox | Isolated Feature Test",
        page_icon="🛡️",
        layout="wide"
    )

    st.title("🛡️ Sandbox: Talent Reconnaissance Engine")
    st.markdown("### Isolated Feature Test - Dynamic Veteran Targeting & Boolean Vectors")

    # --- INPUT CONTROL PANEL ---
    st.markdown("#### 🎯 Enter Operational Search Parameters")
    with st.form(key="sandbox_recon_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            target_company = st.text_input("Target Company", value="GE Aerospace", placeholder="e.g., GE Aerospace, Lockheed Martin")
        with col2:
            target_position = st.text_input("Target Position / Role", value="Sr AI Data Engineer", placeholder="e.g., Sr AI Data Engineer, Cloud Architect")
        with col3:
            target_location = st.text_input("Target Location", value="Greenville, SC", placeholder="e.g., Greenville, SC, Remote")
            
        f_subcol1, f_subcol2 = st.columns(2)
        with f_subcol1:
            branch_filter = st.selectbox(
                "Branch Filter",
                ["All Veterans", "US Army (Special Forces / 18F / 18Z)", "US Air Force", "US Navy", "US Marine Corps", "US Space Force"],
                index=0
            )
        with f_subcol2:
            veteran_only = st.checkbox("Enforce Veteran Status Only", value=True)
            
        submit_button = st.form_submit_button(label="⚡ Execute Sandbox Recon Search", use_container_width=True)

    # --- EXECUTION LOGIC ---
    df = load_sandbox_ledger()
    mask = pd.Series([True] * len(df))

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

    if veteran_only:
        mask &= (df['is_veteran'] == True)

    if branch_filter and branch_filter != "All Veterans":
        clean_branch = branch_filter.split("(")[0].strip()
        mask &= df['branch'].str.contains(re.escape(clean_branch), case=False, na=False)

    results = df[mask].copy()

    # Render Results
    st.markdown("---")
    st.subheader(f"📊 Sandbox Acquisition Results ({len(results)} targets matched)")

    if not results.empty:
        st.dataframe(results[['name', 'company', 'title', 'location', 'branch', 'clearance', 'skills']], use_container_width=True)
    else:
        st.warning("[!] Sandbox query returned zero matches in local dataset. Try expanding search coordinates.")

    # Dynamic Boolean Search Links
    st.markdown("---")
    st.subheader("📡 Live Web Boolean X-Ray Vectors")
    b_query = generate_sandbox_boolean_query(target_company, target_position, target_location, branch_filter)
    st.code(b_query, language="text")

    encoded_q = urllib.parse.quote_plus(b_query)
    g_url = f"https://www.google.com/search?q={encoded_q}"
    d_url = f"https://duckduckgo.com/?q={encoded_q}"
    li_url = f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote_plus(f'{target_company} {target_position} Veteran {target_location}')}&origin=GLOBAL_SEARCH_HEADER"

    b1, b2, b3 = st.columns(3)
    with b1:
        st.link_button("🚀 Launch Google X-Ray Search", g_url, use_container_width=True)
    with b2:
        st.link_button("🦆 Launch DuckDuckGo X-Ray", d_url, use_container_width=True)
    with b3:
        st.link_button("🔗 Direct LinkedIn Search", li_url, use_container_width=True)

    st.markdown("""
    ---
    > 🎯 **Gunslinger Lore: Building in the Trench**  
    > *Before you take a new weapon system to the front lines, you test it in the trench. Sandbox isolation keeps the perimeter secure and your production line undisturbed while you calibrate your dynamic targeting algorithms.*
    """)

if __name__ == "__main__":
    run_streamlit_app()
