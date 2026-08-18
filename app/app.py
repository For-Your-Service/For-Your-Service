# ============================================================================
# For Your Service - Veteran Intake & Job Matching Portal
# 7 Eagle Group - AI-Powered Veteran Placement Platform
# ============================================================================

import streamlit as st
import pandas as pd
import uuid
import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

# Initialize Spark session for Unity Catalog access
try:
    spark = SparkSession.builder.getOrCreate()
except:
    st.error("⚠️ Unable to connect to Databricks compute. Please ensure serverless compute is available.")
    st.stop()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="For Your Service - Veteran Intake",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for branding
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1e3a8a;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #1e3a8a;
        color: white;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎖️ For Your Service: Veteran Intake Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by 7 Eagle Group | AI-Driven Veteran Job Matching</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# INTAKE FORM
# ============================================================================

with st.form("veteran_intake_form", clear_on_submit=False):
    
    st.subheader("📋 Step 1: Personal & Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *", placeholder="William Free Hall")
    with col2:
        email = st.text_input("Email Address *", placeholder="veteran@example.com")
    
    st.markdown("")
    st.subheader("📍 Step 2: Target Location & Compensation")
    col1, col2, col3 = st.columns(3)
    with col1:
        target_city = st.text_input("Target City *", placeholder="Greenville")
    with col2:
        target_state = st.text_input("Target State (2-letter code) *", placeholder="SC", max_chars=2)
    with col3:
        st.write("")  # Spacing
    
    col1, col2 = st.columns(2)
    with col1:
        salary_min = st.slider(
            "Minimum Desired Salary ($) *",
            min_value=40000,
            max_value=200000,
            value=75000,
            step=5000,
            format="$%d"
        )
    with col2:
        salary_max = st.slider(
            "Maximum Target Salary ($) *",
            min_value=40000,
            max_value=200000,
            value=120000,
            step=5000,
            format="$%d"
        )
    
    st.markdown("")
    st.subheader("📄 Step 3: Resume & Experience")
    st.markdown("*Paste your complete resume text below. Include work history, skills, certifications, and education.*")
    resume_text = st.text_area(
        "Resume Text *",
        height=300,
        placeholder="Paste your resume here...\n\nExample:\nWilliam Free Hall\nDevOps Engineer\n\nEXPERIENCE:\n- AWS Cloud Architect (2020-Present)\n- Army Green Beret Team Sergeant (1999-2017)\n\nSKILLS: AWS, Kubernetes, Python, Terraform, Docker..."
    )
    
    st.markdown("")
    submit_button = st.form_submit_button(label="🚀 Register & Find Matching Jobs", use_container_width=True)

# ============================================================================
# FORM SUBMISSION LOGIC
# ============================================================================

if submit_button:
    # Validation
    if not name or not email or not target_city or not target_state or not resume_text:
        st.error("🚨 Please fill out all required fields (*) before submitting.")
    elif len(target_state) != 2:
        st.error("🚨 Target State must be a 2-letter code (e.g., SC, FL, TX).")
    elif salary_min >= salary_max:
        st.error("🚨 Minimum salary must be less than maximum salary.")
    elif len(resume_text) < 100:
        st.error("🚨 Resume text seems too short. Please provide a complete resume (at least 100 characters).")
    else:
        with st.spinner("🔄 Processing your profile and searching for matching opportunities..."):
            try:
                # Generate unique veteran ID
                veteran_id = str(uuid.uuid4())
                
                # ================================================================
                # BASIC AI RESUME PARSING (Extract keywords)
                # ================================================================
                # In production, this would call an LLM API for structured extraction
                # For now, we'll do basic keyword extraction
                
                resume_lower = resume_text.lower()
                
                # Common tech skills to extract
                skill_keywords = [
                    "aws", "azure", "gcp", "kubernetes", "docker", "terraform",
                    "python", "java", "javascript", "sql", "bash", "powershell",
                    "jenkins", "github", "gitlab", "ci/cd", "devops", "linux",
                    "windows", "ansible", "chef", "puppet", "prometheus", "grafana"
                ]
                
                detected_skills = [skill for skill in skill_keywords if skill in resume_lower]
                
                # Estimate years of experience (simple regex for years)
                import re
                years_pattern = r'(\d+)\+?\s*years?'
                years_matches = re.findall(years_pattern, resume_lower)
                total_years = max([int(y) for y in years_matches], default=5)
                
                # Determine seniority
                if total_years >= 10:
                    seniority = "Senior"
                elif total_years >= 5:
                    seniority = "Mid"
                else:
                    seniority = "Entry"
                
                # Package skills as JSON
                technical_skills_json = json.dumps({
                    "detected_skills": detected_skills,
                    "skill_count": len(detected_skills)
                })
                
                # ================================================================
                # WRITE TO UNITY CATALOG
                # ================================================================
                
                profile_data = spark.createDataFrame([{
                    "veteran_id": veteran_id,
                    "name": name,
                    "email": email,
                    "target_city": target_city,
                    "target_state": target_state.upper(),
                    "total_years": total_years,
                    "seniority_level": seniority,
                    "technical_skills": technical_skills_json,
                    "target_roles": json.dumps(["DevOps Engineer", "Cloud Engineer", "Systems Administrator"]),
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }])
                
                # Write to Unity Catalog table
                profile_data.write \
                    .format("delta") \
                    .mode("append") \
                    .saveAsTable("workspace.fys_silver.veteran_profiles")
                
                st.success(f"✅ Profile registered successfully for **{name}** (ID: `{veteran_id}`)")
                
                # ================================================================
                # TRIGGER MATCHING ENGINE NOTEBOOK
                # ================================================================
                
                st.info("🧠 Running AI matching engine against 670+ job postings...")
                
                # Note: dbutils.notebook.run is not available in Streamlit apps
                # Instead, we'll query the job postings directly and do basic matching
                
                # Query job postings from bronze table
                jobs_df = spark.sql(f"""
                    SELECT 
                        job_id,
                        title,
                        company,
                        source,
                        location.city as city,
                        location.state as state,
                        location.display as location_display,
                        salary.min as salary_min,
                        salary.max as salary_max,
                        description,
                        url
                    FROM workspace.fys_bronze.job_postings
                    WHERE location.state = '{target_state.upper()}'
                      AND salary.max >= {salary_min}
                      AND salary.min <= {salary_max}
                    LIMIT 100
                """)
                
                jobs_pdf = jobs_df.toPandas()
                
                if len(jobs_pdf) == 0:
                    st.warning(f"⚠️ No jobs found in {target_city}, {target_state} matching your salary range. Try expanding your search criteria.")
                else:
                    # ================================================================
                    # BASIC KEYWORD MATCHING ALGORITHM
                    # ================================================================
                    
                    def calculate_match_score(job_row):
                        score = 0
                        
                        # Combine job text
                        job_text = ' '.join([
                            str(job_row['title']),
                            str(job_row['description']) if pd.notna(job_row['description']) else ''
                        ]).lower()
                        
                        # Skills match (40 points)
                        skills_matched = sum(1 for skill in detected_skills if skill in job_text)
                        score += min(40, skills_matched * 5)
                        
                        # Salary match (30 points)
                        if pd.notna(job_row['salary_min']) and pd.notna(job_row['salary_max']):
                            if job_row['salary_min'] <= salary_max and job_row['salary_max'] >= salary_min:
                                score += 30
                        
                        # Title match (20 points)
                        target_titles = ['devops', 'cloud', 'engineer', 'architect', 'sre']
                        title_lower = str(job_row['title']).lower()
                        if any(t in title_lower for t in target_titles):
                            score += 20
                        
                        # Location exact match bonus (10 points)
                        if str(job_row['city']).lower() == target_city.lower():
                            score += 10
                        
                        return min(100, score)
                    
                    jobs_pdf['match_score'] = jobs_pdf.apply(calculate_match_score, axis=1)
                    jobs_pdf = jobs_pdf.sort_values('match_score', ascending=False)
                    
                    # ================================================================
                    # DISPLAY TOP MATCHES
                    # ================================================================
                    
                    st.markdown("---")
                    st.subheader("🎯 Top Matching Opportunities")
                    st.markdown(f"Found **{len(jobs_pdf)}** jobs in **{target_state}** matching your criteria. Showing top 10:")
                    
                    top_10 = jobs_pdf.head(10)
                    
                    for idx, (_, job) in enumerate(top_10.iterrows(), 1):
                        with st.expander(f"**#{idx} - {job['title']}** at {job['company']} | Score: {job['match_score']:.0f}/100"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**📍 Location:** {job['city']}, {job['state']}")
                                st.markdown(f"**💰 Salary:** ${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}")
                                st.markdown(f"**📊 Source:** {job['source']}")
                                
                                if pd.notna(job['description']):
                                    desc_snippet = job['description'][:250].replace('\n', ' ')
                                    st.markdown(f"**📝 Description:** {desc_snippet}...")
                            
                            with col2:
                                st.metric("Match Score", f"{job['match_score']:.0f}/100")
                                if pd.notna(job['url']):
                                    st.link_button("🔗 Apply Now", job['url'], use_container_width=True)
                    
                    st.markdown("---")
                    st.success("✅ Matching complete! Review the opportunities above and click 'Apply Now' to submit your application.")
                    
                    # Export results
                    st.download_button(
                        label="📥 Download Full Results (CSV)",
                        data=top_10[['title', 'company', 'city', 'state', 'salary_min', 'salary_max', 'match_score', 'url']].to_csv(index=False),
                        file_name=f"job_matches_{veteran_id[:8]}.csv",
                        mime="text/csv"
                    )
            
            except Exception as e:
                st.error(f"🚨 An error occurred during processing: {str(e)}")
                st.exception(e)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    Powered by <strong>7 Eagle Group</strong> | For Your Service Platform<br>
    AI-Driven Veteran Job Matching | Free Hall - Lead Developer<br>
    🎖️ Serving Those Who Served 🎖️
</div>
""", unsafe_allow_html=True)