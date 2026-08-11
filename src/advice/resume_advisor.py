"""Resume tailoring recommendations."""
from typing import List
from .models import Recommendation, RecommendationType, GapAnalysis

class ResumeAdvisor:
    """Generate resume tailoring advice."""
    
    def generate_recommendations(self, gap_analysis: GapAnalysis) -> List[Recommendation]:
        """Create resume improvement recommendations."""
        recs = []
        
        # Missing skills that candidate might actually have
        for skill_gap in gap_analysis.missing_skills[:5]:
            recs.append(Recommendation(
                type=RecommendationType.RESUME_TAILORING,
                title=f"Highlight {skill_gap.skill_name} experience",
                description=f"This role requires '{skill_gap.skill_name}'. Review your work history for related experience and make it explicit.",
                impact=15,
                priority=2,
                effort="low",
                action_items=[
                    f"Search resume for {skill_gap.skill_name}-related work",
                    "Add specific bullet point highlighting this skill",
                    "Quantify impact with metrics if possible"
                ]
            ))
        
        return recs
