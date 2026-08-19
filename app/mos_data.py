"""
Military Occupational Specialty (MOS / AFSC / Rating) Database & Crosswalk
For Your Service - 7 Eagle Group
Maps military specialties across all service branches to civilian occupations and transferable skills.
"""

from typing import Dict, List, Optional

MOS_DATABASE: Dict[str, Dict] = {
    # =========================================================================
    # U.S. ARMY
    # =========================================================================
    "18Z": {
        "branch": "Army",
        "title": "Special Forces Senior Sergeant / Operations Team Sergeant",
        "civilian_titles": ["Director of Operations", "Senior Solutions Architect", "Enterprise Program Manager", "Chief of Staff"],
        "transferable_skills": ["executive leadership", "strategic planning", "crisis management", "cross-functional operations", "risk assessment", "mission planning", "stakeholder management"],
        "tech_skills": ["data analytics", "satellite communications", "command & control systems", "operations research"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Special Operations / Leadership"
    },
    "18F": {
        "branch": "Army",
        "title": "Special Forces Assistant Operations and Intelligence Sergeant",
        "civilian_titles": ["Intelligence Operations Lead", "Threat Intelligence Architect", "Solutions Architect", "Data Analytics Lead"],
        "transferable_skills": ["intelligence analysis", "link analysis", "executive data briefings", "threat modeling", "inter-agency coordination", "OPSEC", "risk mitigation"],
        "tech_skills": ["palantir", "i2 analyst notebook", "python", "data pipelines", "geospatial intelligence", "sql"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Special Operations / Intelligence"
    },
    "18E": {
        "branch": "Army",
        "title": "Special Forces Communications Sergeant",
        "civilian_titles": ["Telecommunications Engineer", "Network Architect", "Systems Administrator", "Field Support Engineer"],
        "transferable_skills": ["tactical communications", "troubleshooting", "satellite systems", "hardware maintenance", "field operations"],
        "tech_skills": ["rf communications", "satcom", "networking", "cisco", "cryptography", "voip", "antennas"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Special Operations / Communications"
    },
    "18B": {
        "branch": "Army",
        "title": "Special Forces Weapons Sergeant",
        "civilian_titles": ["Security Operations Manager", "Logistics & Armory Director", "Tactical Trainer", "Risk Consultant"],
        "transferable_skills": ["weapons systems", "tactical training", "risk management", "physical security", "instructional design"],
        "tech_skills": ["inventory management", "ballistics modeling", "security protocols"],
        "typical_clearance": "Secret",
        "category": "Special Operations / Combat"
    },
    "18C": {
        "branch": "Army",
        "title": "Special Forces Engineer Sergeant",
        "civilian_titles": ["Civil Project Manager", "Infrastructure Engineer", "Facilities Director", "Field Engineering Lead"],
        "transferable_skills": ["structural analysis", "explosives safety", "demolition", "construction management", "resource planning"],
        "tech_skills": ["cad", "structural modeling", "construction estimating", "quality control"],
        "typical_clearance": "Secret",
        "category": "Special Operations / Engineering"
    },
    "18D": {
        "branch": "Army",
        "title": "Special Forces Medical Sergeant",
        "civilian_titles": ["Physician Assistant (PA)", "Emergency Medical Director", "Clinical Operations Manager", "Trauma Specialist"],
        "transferable_skills": ["trauma medicine", "surgical procedures", "pharmacology", "triage", "public health assessment", "emergency response"],
        "tech_skills": ["electronic health records", "medical equipment diagnostic", "telemedicine"],
        "typical_clearance": "Secret",
        "category": "Special Operations / Medical"
    },
    "25B": {
        "branch": "Army",
        "title": "Information Technology Specialist",
        "civilian_titles": ["IT Support Specialist", "Systems Administrator", "Network Administrator", "Cloud Support Engineer"],
        "transferable_skills": ["hardware troubleshooting", "user support", "system configuration", "network administration", "it service management"],
        "tech_skills": ["windows server", "active directory", "cisco", "linux", "tcp/ip", "powershell", "virtualization", "dns", "dhcp"],
        "typical_clearance": "Secret",
        "category": "Information Technology"
    },
    "25D": {
        "branch": "Army",
        "title": "Cyber Network Defender",
        "civilian_titles": ["Cybersecurity Analyst", "SOC Analyst", "Security Engineer", "Incident Responder"],
        "transferable_skills": ["incident handling", "vulnerability assessment", "threat detection", "security monitoring", "compliance"],
        "tech_skills": ["siem", "splunk", "wireshark", "ids/ips", "firewalls", "penetration testing", "nist framework", "cissp"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Cybersecurity"
    },
    "17C": {
        "branch": "Army",
        "title": "Cyber Operations Specialist",
        "civilian_titles": ["Offensive Security Engineer", "Penetration Tester", "Cyber Threat Hunter", "Reverse Engineer"],
        "transferable_skills": ["offensive security", "exploit development", "threat emulation", "forensics", "reverse engineering"],
        "tech_skills": ["python", "c/c++", "ghidra", "metasploit", "wireshark", "linux kernel", "assembly", "network protocols"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Cybersecurity"
    },
    "35F": {
        "branch": "Army",
        "title": "Intelligence Analyst",
        "civilian_titles": ["Business Intelligence Analyst", "Threat Intelligence Analyst", "Operations Research Analyst", "Data Analyst"],
        "transferable_skills": ["intelligence preparation", "link analysis", "risk assessment", "executive reporting", "data synthesis"],
        "tech_skills": ["palantir", "arcgis", "sql", "excel", "tableau", "data visualization", "predictive modeling"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    },
    "35M": {
        "branch": "Army",
        "title": "Human Intelligence Collector",
        "civilian_titles": ["Investigator", "Corporate Compliance Officer", "Talent Acquisition Specialist", "Negotiator"],
        "transferable_skills": ["interpersonal interviewing", "debriefing", "source management", "cross-cultural communication", "negotiation"],
        "tech_skills": ["investigative databases", "case management systems", "foreign languages"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    },
    "92A": {
        "branch": "Army",
        "title": "Automated Logistical Specialist",
        "civilian_titles": ["Supply Chain Analyst", "Warehouse Operations Manager", "Logistics Coordinator", "Inventory Controller"],
        "transferable_skills": ["supply chain optimization", "inventory auditing", "fleet tracking", "procurement", "shipping & receiving"],
        "tech_skills": ["sap", "erp systems", "excel", "wms (warehouse management systems)", "sql"],
        "typical_clearance": "Secret",
        "category": "Logistics & Supply Chain"
    },
    "92Y": {
        "branch": "Army",
        "title": "Unit Supply Specialist",
        "civilian_titles": ["Inventory Specialist", "Property Manager", "Asset Manager", "Procurement Clerk"],
        "transferable_skills": ["property accountability", "asset tracking", "budget reconciliation", "vendor coordination"],
        "tech_skills": ["inventory databases", "excel", "erp software"],
        "typical_clearance": "Secret",
        "category": "Logistics & Supply Chain"
    },
    "68W": {
        "branch": "Army",
        "title": "Combat Medic Specialist",
        "civilian_titles": ["Emergency Medical Technician (EMT)", "Paramedic", "Clinical Care Specialist", "Healthcare Administrator"],
        "transferable_skills": ["emergency trauma care", "patient triage", "medical documentation", "critical decision making", "vital signs"],
        "tech_skills": ["electronic medical records (emr)", "defibrillator operation", "telehealth tools"],
        "typical_clearance": "Secret",
        "category": "Healthcare & Medical"
    },
    "11B": {
        "branch": "Army",
        "title": "Infantryman",
        "civilian_titles": ["Operations Supervisor", "Field Service Manager", "Physical Security Director", "Project Lead"],
        "transferable_skills": ["team leadership", "tactical planning", "high-stress decision making", "risk management", "adaptability", "equipment operations"],
        "tech_skills": ["digital mapping", "field communications", "standard operating procedures (sop)"],
        "typical_clearance": "Secret",
        "category": "Combat / Operations"
    },
    "88M": {
        "branch": "Army",
        "title": "Motor Transport Operator",
        "civilian_titles": ["Fleet Logistics Manager", "Commercial Driver (CDL)", "Transportation Dispatcher", "Distribution Lead"],
        "transferable_skills": ["heavy vehicle operations", "route planning", "preventive maintenance", "cargo transport safety"],
        "tech_skills": ["fleet telematics", "gps dispatch systems", "dot compliance"],
        "typical_clearance": "Secret",
        "category": "Logistics & Transportation"
    },

    # =========================================================================
    # U.S. NAVY
    # =========================================================================
    "IT": {
        "branch": "Navy",
        "title": "Information Systems Technician",
        "civilian_titles": ["Network Engineer", "Systems Administrator", "Cloud Support Engineer", "Cybersecurity Specialist"],
        "transferable_skills": ["network architecture", "system administration", "satellite communications", "cyber defense", "disaster recovery"],
        "tech_skills": ["cisco routing & switching", "active directory", "linux", "aws", "vmware", "voip", "comsec"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Information Technology"
    },
    "CTN": {
        "branch": "Navy",
        "title": "Cryptologic Technician Networks",
        "civilian_titles": ["Cyber Threat Intelligence Analyst", "Penetration Tester", "Network Security Engineer", "SOC Lead"],
        "transferable_skills": ["network forensics", "cyber warfare", "vulnerability research", "traffic analysis", "incident mitigation"],
        "tech_skills": ["wireshark", "python", "snort", "linux", "cryptography", "reverse engineering", "metasploit"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Cybersecurity"
    },
    "IS": {
        "branch": "Navy",
        "title": "Intelligence Specialist",
        "civilian_titles": ["All-Source Intelligence Analyst", "Geospatial Analyst", "Risk & Security Analyst", "Operations Consultant"],
        "transferable_skills": ["intelligence briefs", "imagery analysis", "geopolitical risk assessment", "target analysis", "command briefs"],
        "tech_skills": ["arcgis", "palantir", "sql", "photoshop", "intelligence databases", "powerpoint"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    },
    "ET": {
        "branch": "Navy",
        "title": "Electronics Technician",
        "civilian_titles": ["Field Electronics Engineer", "Radar Systems Technician", "Telecommunications Specialist", "Hardware Tech"],
        "transferable_skills": ["electronic troubleshooting", "radar/sonar maintenance", "circuit analysis", "rf systems", "preventive maintenance"],
        "tech_skills": ["oscilloscopes", "schematic reading", "soldering", "rf spectrum analyzers", "fiber optics"],
        "typical_clearance": "Secret",
        "category": "Engineering & Electronics"
    },
    "HM": {
        "branch": "Navy",
        "title": "Hospital Corpsman",
        "civilian_titles": ["Clinical Nurse Assistant", "Paramedic", "Medical Operations Manager", "Surgical Technologist"],
        "transferable_skills": ["patient assessment", "field trauma care", "surgical assisting", "preventive medicine", "medical admin"],
        "tech_skills": ["emr/ehr software", "vital monitors", "clinical lab equipment"],
        "typical_clearance": "Secret",
        "category": "Healthcare & Medical"
    },

    # =========================================================================
    # U.S. AIR FORCE / SPACE FORCE
    # =========================================================================
    "1D7X1": {
        "branch": "Air Force",
        "title": "Cyber Defense Operations (formerly 3D0X2 / 3D1X2)",
        "civilian_titles": ["Cloud Systems Engineer", "DevOps Engineer", "Network Infrastructure Lead", "Cyber Operations Analyst"],
        "transferable_skills": ["enterprise network operations", "server virtualization", "cloud migration", "cyber defense", "incident remediation"],
        "tech_skills": ["aws", "azure", "kubernetes", "cisco", "linux", "windows server", "python", "ansible", "security+"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Information Technology / Cloud"
    },
    "1B4X1": {
        "branch": "Air Force",
        "title": "Cyber Warfare Operations Specialist",
        "civilian_titles": ["Principal Cyber Security Engineer", "Red Team Lead", "Exploit Analyst", "Cloud Security Architect"],
        "transferable_skills": ["defensive & offensive cyber operations", "threat hunting", "digital forensics", "malware analysis"],
        "tech_skills": ["python", "c", "assembly", "bash", "splunk", "elastic stack", "ghidra", "mitre att&ck"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Cybersecurity"
    },
    "1N0X1": {
        "branch": "Air Force",
        "title": "All-Source Intelligence Analyst",
        "civilian_titles": ["Senior Intelligence Analyst", "Strategic Risk Consultant", "Data Operations Specialist", "Business Analyst"],
        "transferable_skills": ["mission intelligence briefings", "threat synthesis", "critical thinking", "data-driven reporting"],
        "tech_skills": ["palantir", "arcgis", "tableau", "excel", "power bi", "sql"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    },
    "5C0X1": {
        "branch": "Space Force",
        "title": "Cyber Space Operations Specialist",
        "civilian_titles": ["Satellite Network Engineer", "Space Systems Security Architect", "Cloud Security Engineer"],
        "transferable_skills": ["space network defense", "satellite payload communications", "orbital cyber ops", "telemetry security"],
        "tech_skills": ["satellite link protocols", "linux", "cloud security", "python", "rf analysis", "zero trust"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Space & Cyber"
    },

    # =========================================================================
    # U.S. MARINE CORPS
    # =========================================================================
    "0671": {
        "branch": "Marine Corps",
        "title": "Data Systems Administrator",
        "civilian_titles": ["Systems Administrator", "Cloud Infrastructure Engineer", "IT Operations Lead", "DevOps Specialist"],
        "transferable_skills": ["expeditionary server deployment", "virtualization", "system recovery", "directory services", "tactical networks"],
        "tech_skills": ["vmware", "active directory", "windows server", "linux", "cisco", "powershell", "storage area networks (san)"],
        "typical_clearance": "Secret",
        "category": "Information Technology"
    },
    "0689": {
        "branch": "Marine Corps",
        "title": "Cybersecurity Technician",
        "civilian_titles": ["Information Assurance Officer", "Cybersecurity Engineer", "Compliance Analyst", "SOC Analyst"],
        "transferable_skills": ["ia vulnerability management (iavm)", "security auditing", "risk mitigation", "network monitoring"],
        "tech_skills": ["nessus", "accreditation packages (rmf)", "firewalls", "siem", "wireshark", "security+", "cissp"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Cybersecurity"
    },
    "0311": {
        "branch": "Marine Corps",
        "title": "Rifleman",
        "civilian_titles": ["Operations Supervisor", "Field Logistics Coordinator", "Security Specialist", "Team Leader"],
        "transferable_skills": ["discipline", "leadership in ambiguity", "high-tempo execution", "situational awareness", "team cohesion"],
        "tech_skills": ["tactical radio systems", "sop compliance", "risk assessment"],
        "typical_clearance": "Secret",
        "category": "Combat / Operations"
    },

    # =========================================================================
    # U.S. COAST GUARD
    # =========================================================================
    "CG-IT": {
        "branch": "Coast Guard",
        "title": "Information Systems Technician (CG)",
        "civilian_titles": ["Maritime IT Specialist", "Network Administrator", "Systems Support Engineer"],
        "transferable_skills": ["maritime communications", "server administration", "endpoint management", "troubleshooting"],
        "tech_skills": ["cisco", "active directory", "windows server", "voip", "satcom"],
        "typical_clearance": "Secret",
        "category": "Information Technology"
    },
    "CG-IS": {
        "branch": "Coast Guard",
        "title": "Intelligence Specialist (CG)",
        "civilian_titles": ["Maritime Intelligence Analyst", "Border & Port Security Analyst", "Threat Investigator"],
        "transferable_skills": ["maritime domain awareness", "counter-narcotics intelligence", "threat tracking", "inter-agency reporting"],
        "tech_skills": ["gis mapping", "link analysis", "palantir", "intelligence databases"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    }
}


def lookup_mos(query: str) -> Optional[Dict]:
    """
    Look up an MOS code or search by keyword across military specialties.
    Case-insensitive.
    """
    if not query:
        return None
    
    clean_query = query.strip().upper()
    
    # Direct exact match on code
    if clean_query in MOS_DATABASE:
        result = MOS_DATABASE[clean_query].copy()
        result["code"] = clean_query
        return result
    
    # Strip common prefixes/suffixes (e.g., "MOS 18F" -> "18F")
    for word in clean_query.split():
        if word in MOS_DATABASE:
            result = MOS_DATABASE[word].copy()
            result["code"] = word
            return result
            
    # Fuzzy search on title or transferable skills
    query_lower = query.lower()
    for code, data in MOS_DATABASE.items():
        if query_lower in data["title"].lower() or any(query_lower in s.lower() for s in data["transferable_skills"]):
            result = data.copy()
            result["code"] = code
            return result
            
    return None


def get_all_mos_choices() -> List[str]:
    """Get list of formatted MOS choices for UI dropdowns"""
    choices = []
    for code, data in MOS_DATABASE.items():
        choices.append(f"{code} - {data['title']} ({data['branch']})")
    return sorted(choices)
