#!/usr/bin/env python3
"""
Example Usage: End-to-End Job Matching Pipeline

Demonstrates complete veteran job matching flow from resume to recommendations.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from src.pipeline import MatchingOrchestrator

def main():
    """Run example matching pipeline"""
    
    print("=" * 60)
    print("For Your Service - Veteran Job Matching Pipeline")
    print("=" * 60)
    print()
    
    # Initialize orchestrator
    print("Initializing orchestrator...")
    orchestrator = MatchingOrchestrator(
        similarity_threshold=0.6,
        enable_military_mapping=True
    )
    print("✓ Orchestrator ready")
    print()
    
    # Define target jobs (example: DevOps Engineer roles)
    print("Loading job requirements...")
    jobs = [
        {
            "id": "job1",
            "title": "DevOps Engineer",
            "company": "Tech Innovations Inc",
            "location": "Greenville, SC",
            "salary_range": "$120K-$180K",
            "veteran_friendly": True,
            "required_skills": [
                {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
                {"skill": "Kubernetes", "importance": "Critical", "required_level": "Proficient"},
                {"skill": "Terraform", "importance": "Important", "required_level": "Proficient"},
                {"skill": "Python", "importance": "Important", "required_level": "Proficient"},
                {"skill": "Docker", "importance": "Important", "required_level": "Proficient"},
                {"skill": "Jenkins", "importance": "Nice-to-have", "required_level": "Proficient"}
            ]
        },
        {
            "id": "job2",
            "title": "Cloud Solutions Architect",
            "company": "Enterprise Solutions LLC",
            "location": "Remote",
            "salary_range": "$150K-$200K",
            "veteran_friendly": True,
            "required_skills": [
                {"skill": "AWS", "importance": "Critical", "required_level": "Expert"},
                {"skill": "Azure", "importance": "Important", "required_level": "Proficient"},
                {"skill": "Terraform", "importance": "Critical", "required_level": "Proficient"},
                {"skill": "Kubernetes", "importance": "Important", "required_level": "Proficient"},
                {"skill": "Python", "importance": "Nice-to-have", "required_level": "Proficient"}
            ]
        },
        {
            "id": "job3",
            "title": "Site Reliability Engineer",
            "company": "Defense Contractors Group",
            "location": "Greenville, SC",
            "salary_range": "$130K-$170K",
            "veteran_friendly": True,
            "clearance_required": True,
            "required_skills": [
                {"skill": "Linux", "importance": "Critical", "required_level": "Expert"},
                {"skill": "Python", "importance": "Critical", "required_level": "Proficient"},
                {"skill": "Kubernetes", "importance": "Important", "required_level": "Proficient"},
                {"skill": "Monitoring", "importance": "Important", "required_level": "Proficient"},
                {"skill": "AWS", "importance": "Nice-to-have", "required_level": "Proficient"}
            ]
        }
    ]
    print(f"✓ Loaded {len(jobs)} job opportunities")
    print()
    
    # Process resume
    resume_path = "examples/sample_veteran_resume.pdf"
    print(f"Processing resume: {resume_path}")
    print("(Note: Use actual resume file for real matching)")
    print()
    
    # Example: Show what the results would look like
    print("=" * 60)
    print("EXAMPLE OUTPUT (with mock data)")
    print("=" * 60)
    print()
    
    print("📋 CANDIDATE PROFILE")
    print("-" * 60)
    print("Name: Free Hall")
    print("Email: whall4.wh@gmail.com")
    print("Location: Greenville, SC")
    print("Experience: 18 years")
    print()
    print("Military Background:")
    print("  Branch: Army")
    print("  MOS: 18Z (Special Forces Team Sergeant)")
    print("  Clearance: TS/SCI (expired)")
    print()
    print("Skills:")
    print("  • AWS, Azure, Kubernetes, Docker, Terraform")
    print("  • Python, Bash, Jenkins, GitHub")
    print("  • Leadership, Strategic Planning, Team Management")
    print("  • Network Administration, Cybersecurity")
    print()
    
    print("=" * 60)
    print("JOB MATCH RESULTS")
    print("=" * 60)
    print()
    
    # Mock results for Job 1
    print("1️⃣  DevOps Engineer - Tech Innovations Inc")
    print("    Location: Greenville, SC")
    print("    Salary: $120K-$180K")
    print("    🎖️  Veteran-Friendly Employer")
    print()
    print("    Match Score: 85%")
    print("    ✓ Matching Skills (5): AWS, Kubernetes, Python, Docker, Terraform")
    print("    ⚠ Missing Skills (1): Jenkins")
    print()
    print("    📊 Gap Analysis:")
    print("       - Jenkins: Nice-to-have | ~2-3 weeks to learn")
    print("       - Recommendation: APPLY NOW - Strong match!")
    print()
    print("    🎯 Readiness: Ready to apply immediately")
    print()
    
    # Mock results for Job 2
    print("2️⃣  Cloud Solutions Architect - Enterprise Solutions LLC")
    print("    Location: Remote")
    print("    Salary: $150K-$200K")
    print("    🎖️  Veteran-Friendly Employer")
    print()
    print("    Match Score: 72%")
    print("    ✓ Matching Skills (4): AWS, Terraform, Kubernetes, Python")
    print("    ⚠ Missing Skills (1): Azure")
    print()
    print("    📊 Gap Analysis:")
    print("       - Azure: Important | ~4-6 weeks to learn")
    print("       - Recommendation: Build Azure foundations first")
    print()
    print("    🎯 Readiness: 1-2 months with Azure upskilling")
    print()
    
    # Mock results for Job 3
    print("3️⃣  Site Reliability Engineer - Defense Contractors Group")
    print("    Location: Greenville, SC")
    print("    Salary: $130K-$170K")
    print("    🎖️  Veteran-Friendly Employer")
    print("    🔒 Clearance Required")
    print()
    print("    Match Score: 78%")
    print("    ✓ Matching Skills (4): Python, Kubernetes, AWS, Linux")
    print("    ⚠ Missing Skills (1): Monitoring (Prometheus/Grafana)")
    print()
    print("    📊 Gap Analysis:")
    print("       - Monitoring: Important | ~2-4 weeks to learn")
    print("       - Note: Expired clearance may be renewable")
    print()
    print("    🎯 Readiness: Ready now (highlight clearance history)")
    print()
    
    print("=" * 60)
    print("PERSONALIZED RECOMMENDATIONS")
    print("=" * 60)
    print()
    
    print("📝 Resume Improvements:")
    print("  1. Add professional summary highlighting 18 years of experience")
    print("  2. Translate '18Z' to 'Special Forces Team Sergeant'")
    print("  3. Quantify achievements: team sizes, infrastructure scale")
    print("  4. Add certifications: AWS Solutions Architect, CKA")
    print()
    
    print("🎯 Job Search Strategy:")
    print("  • Target veteran-friendly employers (all 3 matches qualify)")
    print("  • Emphasize security clearance history (defense contractors)")
    print("  • Apply to DevOps role immediately (85% match)")
    print("  • Leverage 18+ years experience for senior/lead positions")
    print()
    
    print("🤝 Networking Advice:")
    print("  • Join Hire Heroes USA for resume review")
    print("  • Connect with 7 Eagle Group veteran network")
    print("  • Attend Greenville tech meetups")
    print("  • Reach out to veteran hiring managers on LinkedIn")
    print()
    
    print("📚 Skill Development Plan:")
    print("  Priority 1: Azure basics (4-6 weeks)")
    print("    - Microsoft Azure Administrator Associate cert")
    print("    - Azure free tier hands-on labs")
    print()
    print("  Priority 2: Jenkins CI/CD (2-3 weeks)")
    print("    - Jenkins official tutorials")
    print("    - Build sample CI/CD pipeline on GitHub")
    print()
    print("  Priority 3: Monitoring stack (2-4 weeks)")
    print("    - Prometheus & Grafana tutorials")
    print("    - Deploy monitoring for personal projects")
    print()
    
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print()
    print("✅ 1. Update resume with recommendations above")
    print("✅ 2. Apply to DevOps Engineer role (Tech Innovations)")
    print("✅ 3. Start Azure learning path (for Solutions Architect role)")
    print("✅ 4. Join 7 Eagle Group networking events")
    print("✅ 5. Reach out to 5 veteran hiring managers on LinkedIn")
    print()
    print("🎯 Timeline: Ready to apply now, full skill coverage in 2-3 months")
    print()


if __name__ == "__main__":
    main()
