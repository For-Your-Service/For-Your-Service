"""
Recommendation Engine

Generates personalized job search advice and resume improvements.
Tailored recommendations for veteran career transitions.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ResumeImprovement:
    """Individual resume improvement suggestion"""
    section: str  # "Skills", "Experience", "Summary", etc.
    issue: str
    suggestion: str
    priority: str  # "High", "Medium", "Low"
    example: Optional[str] = None


@dataclass
class Recommendation:
    """Complete recommendation package"""
    resume_improvements: List[ResumeImprovement]
    job_search_tips: List[str]
    networking_advice: List[str]
    skill_development_plan: List[Dict]
    estimated_timeline: str


class RecommendationEngine:
    """Generates personalized career recommendations"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        
        # Veteran-specific networking advice
        self.veteran_networks = [
            "Join Hire Heroes USA for resume reviews and mock interviews",
            "Connect with American Corporate Partners (ACP) for mentorship",
            "Attend 7 Eagle Group veteran networking events",
            "Join Veterati.com for 1-on-1 veteran mentor matches",
            "Leverage LinkedIn Veterans group for job opportunities"
        ]
        
        # Military-to-civilian resume tips
        self.military_resume_tips = [
            "Translate military jargon to civilian terms",
            "Quantify achievements with metrics and numbers",
            "Remove acronyms that civilians won't understand",
            "Emphasize leadership and team management",
            "Highlight security clearance prominently if active"
        ]
    
    def generate_recommendations(
        self,
        resume_data: Dict,
        gap_analysis: Dict,
        target_jobs: List[Dict]
    ) -> Recommendation:
        """
        Generate comprehensive recommendations
        
        Args:
            resume_data: Parsed resume information
            gap_analysis: Skills gap analysis results
            target_jobs: List of target job postings
            
        Returns:
            Complete recommendation package
        """
        # Analyze resume for improvements
        resume_improvements = self._analyze_resume(resume_data, gap_analysis)
        
        # Generate job search tips
        job_tips = self._generate_job_search_tips(
            resume_data,
            gap_analysis,
            target_jobs
        )
        
        # Networking advice
        networking = self._generate_networking_advice(resume_data)
        
        # Skill development plan
        skill_plan = self._create_skill_development_plan(gap_analysis)
        
        # Timeline estimate
        timeline = self._estimate_timeline(gap_analysis, resume_improvements)
        
        return Recommendation(
            resume_improvements=resume_improvements,
            job_search_tips=job_tips,
            networking_advice=networking,
            skill_development_plan=skill_plan,
            estimated_timeline=timeline
        )
    
    def _analyze_resume(
        self,
        resume_data: Dict,
        gap_analysis: Dict
    ) -> List[ResumeImprovement]:
        """Analyze resume and suggest improvements"""
        improvements = []
        
        # Check summary/objective
        if not resume_data.get("summary"):
            improvements.append(ResumeImprovement(
                section="Summary",
                issue="Missing professional summary",
                suggestion="Add a 2-3 sentence summary highlighting your key skills "
                          "and career goals",
                priority="High",
                example="DevOps Engineer with 10+ years military experience in "
                       "infrastructure, automation, and team leadership. Skilled in "
                       "AWS, Kubernetes, and CI/CD. Seeking cloud engineering role."
            ))
        
        # Check skills section
        candidate_skills = resume_data.get("skills", [])
        if len(candidate_skills) < 5:
            improvements.append(ResumeImprovement(
                section="Skills",
                issue="Limited skills listed",
                suggestion="Expand skills section to 10-15 relevant technical skills",
                priority="High"
            ))
        
        # Military experience translation
        is_veteran = resume_data.get("military_branch") is not None
        if is_veteran:
            improvements.append(ResumeImprovement(
                section="Experience",
                issue="Military terminology may not be clear to civilian recruiters",
                suggestion="Translate military roles to civilian equivalents. "
                          "Replace MOS codes with civilian job titles.",
                priority="High",
                example="Instead of '18E Communications Sergeant', "
                       "use 'Network Systems Manager'"
            ))
        
        # Quantify achievements
        improvements.append(ResumeImprovement(
            section="Experience",
            issue="Need more quantified achievements",
            suggestion="Add metrics: team size, budget managed, systems deployed, "
                      "uptime percentage, cost savings",
            priority="Medium",
            example="Managed infrastructure serving 50K+ users with 99.9% uptime"
        ))
        
        # Missing skills from gap analysis
        missing_critical = [
            g for g in gap_analysis.get("missing_skills", [])
            if g.get("importance") == "Critical"
        ]
        if missing_critical:
            skill_names = [g["skill_name"] for g in missing_critical[:3]]
            improvements.append(ResumeImprovement(
                section="Skills",
                issue=f"Missing critical skills for target roles",
                suggestion=f"Consider adding projects or labs for: {', '.join(skill_names)}",
                priority="High"
            ))
        
        return improvements
    
    def _generate_job_search_tips(
        self,
        resume_data: Dict,
        gap_analysis: Dict,
        target_jobs: List[Dict]
    ) -> List[str]:
        """Generate job search strategy tips"""
        tips = []
        
        # Match score based tips
        match_score = gap_analysis.get("match_score", 0.0)
        
        if match_score >= 0.8:
            tips.append(
                "✓ Strong match! Apply immediately and emphasize your matching skills"
            )
        elif match_score >= 0.6:
            tips.append(
                "Good foundation - Focus applications on roles where you meet "
                "70%+ requirements"
            )
        else:
            tips.append(
                "Build skills first - Consider contract/freelance to gain missing experience"
            )
        
        # Veteran-specific advice
        if resume_data.get("military_branch"):
            tips.extend([
                "Highlight security clearance prominently in headline if active/recent",
                "Use veteran hiring preference programs (VOW Act, VEVRAA)",
                "Target defense contractors and government contractors first"
            ])
        
        # Location-based advice
        location = resume_data.get("location", "")
        if location:
            tips.append(
                f"Target companies in {location} area and highlight relocation flexibility"
            )
        
        # Experience level advice
        total_exp = resume_data.get("total_years_experience", 0)
        if total_exp >= 10:
            tips.append(
                "Emphasize leadership and mentoring - Qualify for senior/lead roles"
            )
        elif total_exp < 3:
            tips.append(
                "Build portfolio projects on GitHub to demonstrate skills"
            )
        
        return tips
    
    def _generate_networking_advice(self, resume_data: Dict) -> List[str]:
        """Generate networking recommendations"""
        advice = []
        
        # Veteran-specific networks
        if resume_data.get("military_branch"):
            advice.extend(self.veteran_networks)
        
        # General networking
        advice.extend([
            "Optimize LinkedIn profile with skills matching target roles",
            "Join relevant Slack/Discord communities (DevOps, Cloud)",
            "Attend local tech meetups and conferences",
            "Reach out to 5 people per week in target companies"
        ])
        
        return advice
    
    def _create_skill_development_plan(
        self,
        gap_analysis: Dict
    ) -> List[Dict]:
        """Create prioritized skill development plan"""
        plan = []
        
        missing_skills = gap_analysis.get("missing_skills", [])
        
        # Sort by importance
        importance_order = {"Critical": 0, "Important": 1, "Nice-to-have": 2}
        sorted_skills = sorted(
            missing_skills,
            key=lambda s: importance_order.get(s.get("importance", "Important"), 3)
        )
        
        for idx, skill in enumerate(sorted_skills[:5], 1):
            plan.append({
                "priority": idx,
                "skill": skill.get("skill_name"),
                "estimated_time": skill.get("estimated_time", "4-6 weeks"),
                "resources": skill.get("learning_resources", []),
                "goal": f"Reach {skill.get('target_level', 'Proficient')} level"
            })
        
        return plan
    
    def _estimate_timeline(
        self,
        gap_analysis: Dict,
        improvements: List[ResumeImprovement]
    ) -> str:
        """Estimate overall timeline to job readiness"""
        match_score = gap_analysis.get("match_score", 0.0)
        high_priority_improvements = sum(
            1 for i in improvements if i.priority == "High"
        )
        
        if match_score >= 0.8 and high_priority_improvements <= 2:
            return "Ready to apply now - 2-4 weeks to interviews"
        elif match_score >= 0.6:
            return "1-2 months: Resume improvements + skill building"
        else:
            return "3-6 months: Comprehensive skill development needed"
