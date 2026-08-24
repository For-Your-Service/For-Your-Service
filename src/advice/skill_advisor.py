"""Skill development recommendations."""
from typing import List
from .models import Recommendation, RecommendationType, GapAnalysis

class SkillAdvisor:
    """Generate skill acquisition advice."""
    
    SKILL_RESOURCES = {
        'kubernetes': ['Kubernetes in Action book', 'CKA certification', 'KodeKloud labs'],
        'terraform': ['HashiCorp Learn', 'Terraform Associate cert', 'Udemy courses'],
        'aws': ['AWS Solutions Architect', 'A Cloud Guru', 'AWS Free Tier labs'],
        'python': ['Python for Everybody', 'Real Python', 'Automate Boring Stuff'],
    }
    
    def generate_recommendations(self, gap_analysis: GapAnalysis) -> List[Recommendation]:
        """Create skill development recommendations."""
        recs = []
        
        for skill_gap in gap_analysis.get_critical_gaps()[:3]:
            skill_name = skill_gap.skill_name.lower()
            resources = self.SKILL_RESOURCES.get(skill_name, ['Search online tutorials'])
            
            recs.append(Recommendation(
                type=RecommendationType.SKILL_GAP,
                title=f"Learn {skill_gap.skill_name}",
                description=f"Critical skill for this role. Acquiring this will increase your match score by ~20%.",
                impact=22,
                priority=1,
                effort="medium",
                action_items=[
                    f"Complete beginner tutorial for {skill_gap.skill_name}",
                    "Build hands-on project",
                    "Add to resume with specific examples"
                ],
                resources=resources
            ))
        
        return recs
