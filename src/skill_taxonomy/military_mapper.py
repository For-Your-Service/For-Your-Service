"""
Military Skill Mapper

Maps Military Occupational Specialties (MOS) to civilian skills.
Supports all branches: Army, Navy, Air Force, Marines, Coast Guard.

Based on veteran experience mapping for 7 Eagle Group job matching.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass


@dataclass
class MilitaryRole:
    """Military occupational specialty"""
    code: str
    branch: str
    title: str
    civilian_equivalent: str
    skills: List[str]
    certifications: List[str]


class MilitarySkillMapper:
    """Maps military experience to civilian skills"""
    
    def __init__(self):
        """Initialize with MOS mappings"""
        
        # Army Special Forces (18 Series) - High priority for 7 Eagle Group
        self.army_mos = {
            "18A": MilitaryRole(
                code="18A",
                branch="Army",
                title="Special Forces Officer",
                civilian_equivalent="Operations Manager / Project Manager",
                skills=[
                    "Leadership", "Strategic Planning", "Risk Management",
                    "Cross-functional Team Management", "Crisis Management",
                    "Foreign Languages", "Cultural Awareness"
                ],
                certifications=["PMP", "Security+"]
            ),
            "18B": MilitaryRole(
                code="18B",
                branch="Army",
                title="Special Forces Weapons Sergeant",
                civilian_equivalent="Technical Specialist / Systems Engineer",
                skills=[
                    "Technical Training", "Systems Analysis", "Problem Solving",
                    "Equipment Maintenance", "Safety Management",
                    "Attention to Detail", "Quality Control"
                ],
                certifications=["Six Sigma", "OSHA Certification"]
            ),
            "18C": MilitaryRole(
                code="18C",
                branch="Army",
                title="Special Forces Engineer Sergeant",
                civilian_equivalent="Civil Engineer / Construction Manager",
                skills=[
                    "Engineering", "Construction", "Project Planning",
                    "Structural Analysis", "Demolition", "Resource Management",
                    "Safety Procedures"
                ],
                certifications=["PE License", "PMP", "OSHA 30"]
            ),
            "18D": MilitaryRole(
                code="18D",
                branch="Army",
                title="Special Forces Medical Sergeant",
                civilian_equivalent="Paramedic / Emergency Medical Technician",
                skills=[
                    "Emergency Medicine", "Trauma Care", "Patient Assessment",
                    "Surgical Procedures", "Pharmacology", "Crisis Response"
                ],
                certifications=["EMT-P", "ACLS", "PALS", "TCCC"]
            ),
            "18E": MilitaryRole(
                code="18E",
                branch="Army",
                title="Special Forces Communications Sergeant",
                civilian_equivalent="Network Engineer / IT Specialist",
                skills=[
                    "Telecommunications", "Network Administration",
                    "Radio Communications", "Satellite Systems",
                    "Encryption", "Troubleshooting", "Cybersecurity"
                ],
                certifications=["Network+", "CCNA", "Security+", "CEH"]
            ),
            "18F": MilitaryRole(
                code="18F",
                branch="Army",
                title="Special Forces Intelligence Sergeant",
                civilian_equivalent="Intelligence Analyst / Data Analyst",
                skills=[
                    "Intelligence Analysis", "Data Collection",
                    "Report Writing", "OSINT", "Threat Assessment",
                    "Critical Thinking", "Research"
                ],
                certifications=["Security+", "CISSP", "Data Analytics"]
            ),
            "18Z": MilitaryRole(
                code="18Z",
                branch="Army",
                title="Special Forces Senior Sergeant",
                civilian_equivalent="Senior Manager / Director of Operations",
                skills=[
                    "Senior Leadership", "Strategic Planning",
                    "Multi-team Coordination", "Budget Management",
                    "Training and Development", "Mentorship"
                ],
                certifications=["PMP", "Leadership Certification"]
            ),
            # Infantry
            "11B": MilitaryRole(
                code="11B",
                branch="Army",
                title="Infantryman",
                civilian_equivalent="Security Specialist / Law Enforcement",
                skills=[
                    "Physical Security", "Tactical Planning",
                    "Team Coordination", "Weapons Proficiency",
                    "Crisis Response", "Attention to Detail"
                ],
                certifications=["Security+", "CPR/First Aid"]
            ),
            # Intelligence
            "35F": MilitaryRole(
                code="35F",
                branch="Army",
                title="Intelligence Analyst",
                civilian_equivalent="Business Intelligence Analyst",
                skills=[
                    "Data Analysis", "Intelligence Collection",
                    "Report Generation", "Pattern Recognition",
                    "Critical Thinking", "Communication"
                ],
                certifications=["Security+", "Data Analytics"]
            ),
            # Signal Corps
            "25B": MilitaryRole(
                code="25B",
                branch="Army",
                title="Information Technology Specialist",
                civilian_equivalent="IT Support Specialist / Systems Administrator",
                skills=[
                    "Network Administration", "Help Desk Support",
                    "Hardware/Software Installation", "Troubleshooting",
                    "Active Directory", "Windows Server", "Linux"
                ],
                certifications=["CompTIA A+", "Network+", "Security+"]
            ),
            "25D": MilitaryRole(
                code="25D",
                branch="Army",
                title="Cyber Network Defender",
                civilian_equivalent="Cybersecurity Analyst",
                skills=[
                    "Cybersecurity", "Network Defense", "Incident Response",
                    "Vulnerability Assessment", "SIEM", "Intrusion Detection"
                ],
                certifications=["Security+", "CEH", "CISSP"]
            ),
        }
        
        # Air Force (AFSC codes)
        self.air_force_afsc = {
            "1N0X1": MilitaryRole(
                code="1N0X1",
                branch="Air Force",
                title="All-Source Intelligence Analyst",
                civilian_equivalent="Intelligence Analyst",
                skills=[
                    "Intelligence Analysis", "Report Writing",
                    "Data Collection", "Threat Assessment"
                ],
                certifications=["Security+", "CISSP"]
            ),
            "3D0X2": MilitaryRole(
                code="3D0X2",
                branch="Air Force",
                title="Cyber Systems Operations",
                civilian_equivalent="Systems Administrator",
                skills=[
                    "Systems Administration", "Network Management",
                    "Server Configuration", "Cybersecurity"
                ],
                certifications=["Security+", "CCNA", "Linux+"]
            ),
        }
        
        # Navy (Rating codes)
        self.navy_ratings = {
            "IT": MilitaryRole(
                code="IT",
                branch="Navy",
                title="Information Systems Technician",
                civilian_equivalent="IT Specialist",
                skills=[
                    "Network Administration", "Systems Support",
                    "Telecommunications", "Troubleshooting"
                ],
                certifications=["Network+", "Security+"]
            ),
            "CTN": MilitaryRole(
                code="CTN",
                branch="Navy",
                title="Cryptologic Technician Networks",
                civilian_equivalent="Cybersecurity Analyst",
                skills=[
                    "Cybersecurity", "Network Defense",
                    "Cryptography", "Penetration Testing"
                ],
                certifications=["CEH", "CISSP", "OSCP"]
            ),
        }
    
    def get_military_role(self, mos_code: str, branch: str) -> Optional[MilitaryRole]:
        """
        Get military role details by MOS/AFSC/Rating code
        
        Args:
            mos_code: Military occupational specialty code
            branch: Military branch (Army, Air Force, Navy, Marines, Coast Guard)
            
        Returns:
            MilitaryRole or None if not found
        """
        mos_upper = mos_code.upper()
        
        if branch.lower() == "army":
            return self.army_mos.get(mos_upper)
        elif branch.lower() == "air force":
            return self.air_force_afsc.get(mos_upper)
        elif branch.lower() == "navy":
            return self.navy_ratings.get(mos_upper)
        
        return None
    
    def extract_civilian_skills(self, mos_code: str, branch: str) -> List[str]:
        """
        Extract civilian skills from military role
        
        Args:
            mos_code: Military occupational specialty code
            branch: Military branch
            
        Returns:
            List of civilian-applicable skills
        """
        role = self.get_military_role(mos_code, branch)
        if role:
            return role.skills
        return []
    
    def get_recommended_certifications(self, mos_code: str, branch: str) -> List[str]:
        """
        Get recommended civilian certifications for military role
        
        Args:
            mos_code: Military occupational specialty code
            branch: Military branch
            
        Returns:
            List of recommended certifications
        """
        role = self.get_military_role(mos_code, branch)
        if role:
            return role.certifications
        return []
    
    def get_civilian_equivalent(self, mos_code: str, branch: str) -> Optional[str]:
        """
        Get civilian job title equivalent
        
        Args:
            mos_code: Military occupational specialty code
            branch: Military branch
            
        Returns:
            Civilian job title or None
        """
        role = self.get_military_role(mos_code, branch)
        if role:
            return role.civilian_equivalent
        return None
    
    def enrich_resume_with_military_skills(self, resume_data: Dict) -> Dict:
        """
        Enrich resume with extracted military-to-civilian skills
        
        Args:
            resume_data: Resume dict with military_branch and military_mos
            
        Returns:
            Enriched resume with additional civilian skills
        """
        military_branch = resume_data.get("military_branch")
        military_mos = resume_data.get("military_mos")
        
        if not military_branch or not military_mos:
            return resume_data
        
        # Extract skills
        military_skills = self.extract_civilian_skills(military_mos, military_branch)
        
        # Merge with existing skills
        existing_skills = resume_data.get("skills", [])
        all_skills = set(existing_skills + military_skills)
        
        # Add recommended certs
        recommended_certs = self.get_recommended_certifications(military_mos, military_branch)
        
        resume_data["skills"] = list(all_skills)
        resume_data["recommended_certifications"] = recommended_certs
        resume_data["civilian_equivalent_title"] = self.get_civilian_equivalent(military_mos, military_branch)
        
        return resume_data
