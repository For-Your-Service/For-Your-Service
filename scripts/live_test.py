#!/usr/bin/env python3
"""
LIVE TEST: Veteran Job Matching with Real Data

This script runs end-to-end matching with:
- REAL jobs from USAJobs API
- YOUR actual resume
- REAL recommendations for veterans

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.integration import LiveMatcher


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_live_test(resume_path: str):
    """
    Run live veteran job matching test
    
    Args:
        resume_path: Path to your resume PDF or DOCX
    """
    print("\n" + "=" * 80)
    print("FOR YOUR SERVICE - LIVE VETERAN JOB MATCHING")
    print("7 Eagle Group")
    print("=" * 80)
    print()
    
    # Verify resume exists
    if not Path(resume_path).exists():
        print(f"❌ Error: Resume not found at {resume_path}")
        print("\nPlease provide the path to your resume:")
        print("  python scripts/live_test.py path/to/your/resume.pdf")
        return
    
    print(f"📄 Resume: {resume_path}")
    print()
    
    # Initialize live matcher
    print("🔧 Initializing live matcher...")
    matcher = LiveMatcher(
        user_email="whall4.wh@gmail.com",
        similarity_threshold=0.6,
        enable_military_mapping=True
    )
    print("✓ Matcher ready")
    print()
    
    # Configure search
    location = "Greenville, SC"
    keywords = ["DevOps", "Cloud Engineer", "Solutions Architect", "Site Reliability", "Platform Engineer"]
    job_limit = 50
    salary_min = 120000  # $120K minimum
    
    print(f"🔍 Search Parameters:")
    print(f"   Location: {location}")
    print(f"   Keywords: {', '.join(keywords)}")
    print(f"   Job Limit: {job_limit}")
    print(f"   Min Salary: ${salary_min:,}")
    print()
    
    print("⏳ Fetching live jobs from USAJobs API...")
    print("   (This may take 10-30 seconds)")
    print()
    
    try:
        # Run live matching
        results = matcher.match_veteran_to_live_jobs(
            resume_path=resume_path,
            location=location,
            keywords=keywords,
            job_limit=job_limit,
            salary_min=salary_min
        )
        
        # Check for errors
        if "error" in results:
            print(f"❌ {results['error']}")
            return
        
        # Display results
        print()
        print("=" * 80)
        print("✅ MATCHING COMPLETE - RESULTS BELOW")
        print("=" * 80)
        print()
        
        display_detailed_results(results)
        
        # Save results
        save_results(results, resume_path)
        
    except Exception as e:
        logger.error(f"Error during matching: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("\nPlease check the logs for details.")


def display_detailed_results(results: dict):
    """Display detailed matching results"""
    
    candidate = results.get("candidate", {})
    gap_analyses = results.get("gap_analyses", [])
    recommendations = results.get("recommendations")
    summary = results.get("summary", {})
    
    # Candidate Profile
    print("📋 CANDIDATE PROFILE")
    print("-" * 80)
    print(f"Name: {candidate.get('name', 'N/A')}")
    print(f"Email: {candidate.get('email', 'N/A')}")
    print(f"Location: {candidate.get('location', 'N/A')}")
    print(f"Experience: {candidate.get('experience_years', 0)} years")
    print(f"Skills ({len(candidate.get('skills', []))}): {', '.join(candidate.get('skills', [])[:10])}")
    
    military = candidate.get("military_background", {})
    if military.get("branch"):
        print(f"\n🎖️  Military Background:")
        print(f"   Branch: {military.get('branch')}")
        print(f"   MOS: {military.get('mos', 'N/A')}")
        if military.get("clearance"):
            print(f"   Clearance: {military.get('clearance')}")
    print()
    
    # Summary Statistics
    print("📊 MATCH SUMMARY")
    print("-" * 80)
    print(f"Jobs Analyzed: {summary.get('total_jobs_analyzed', 0)}")
    print(f"Best Match Score: {summary.get('best_match_score', 0):.1%}")
    print(f"Average Match Score: {summary.get('average_match_score', 0):.1%}")
    print()
    
    # Top 5 Matches
    print("🎯 TOP 5 JOB MATCHES")
    print("-" * 80)
    
    for i, gap_data in enumerate(gap_analyses[:5], 1):
        gap = gap_data.get("gap_analysis")
        job_id = gap_data.get("job_id")
        
        print(f"\n{i}. {gap_data.get('job_title')}")
        print(f"   Job ID: {job_id}")
        print(f"   Match Score: {gap.match_score:.1%}")
        print(f"   Readiness: {gap.estimated_readiness}")
        print(f"   ✓ Matching Skills: {', '.join(gap.matching_skills[:5])}")
        
        if gap.missing_skills:
            missing = [g.skill_name for g in gap.missing_skills[:3]]
            print(f"   ⚠ Missing Skills: {', '.join(missing)}")
    
    print()
    
    # Recommendations
    if recommendations:
        print("💡 PERSONALIZED RECOMMENDATIONS")
        print("-" * 80)
        
        print("\n📝 Resume Improvements:")
        for improvement in recommendations.resume_improvements[:3]:
            print(f"   • {improvement.section}: {improvement.suggestion[:100]}...")
        
        print("\n🎯 Job Search Tips:")
        for tip in recommendations.job_search_tips[:3]:
            print(f"   • {tip}")
        
        print("\n📚 Skill Development Plan:")
        for item in recommendations.skill_development_plan[:3]:
            print(f"   {item['priority']}. {item['skill']} - {item['estimated_time']}")
        
        print()


def save_results(results: dict, resume_path: str):
    """Save results to JSON file"""
    import json
    from datetime import datetime
    
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    resume_name = Path(resume_path).stem
    output_file = output_dir / f"match_results_{resume_name}_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"💾 Results saved to: {output_file}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/live_test.py <path_to_resume.pdf>")
        print("\nExample:")
        print("  python scripts/live_test.py data/resumes/my_resume.pdf")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    run_live_test(resume_path)
