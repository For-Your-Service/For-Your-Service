"""
Military Occupational Specialty (MOS / AFSC / Rating) Database & Crosswalk
For Your Service - 7 Eagle Group
Comprehensive mapping across ALL service branches, ranks, and career fields:
Combat Arms, Logistics, Mechanics, Administration, Medical, Law Enforcement,
Aviation, Intelligence, Communications, Engineering, and Cyber.
"""

from typing import Dict, List, Optional

# Branch specific ranks
BRANCH_RANKS: Dict[str, List[str]] = {
    "Army": [
        "E-1 | Private (PVT)",
        "E-2 | Private Second Class (PV2)",
        "E-3 | Private First Class (PFC)",
        "E-4 | Specialist (SPC) / Corporal (CPL)",
        "E-5 | Sergeant (SGT)",
        "E-6 | Staff Sergeant (SSG)",
        "E-7 | Sergeant First Class (SFC)",
        "E-8 | Master Sergeant (MSG) / First Sergeant (1SG)",
        "E-9 | Sergeant Major (SGM) / Command Sergeant Major (CSM)",
        "W-1 | Warrant Officer 1 (WO1)",
        "W-2 | Chief Warrant Officer 2 (CW2)",
        "W-3 | Chief Warrant Officer 3 (CW3)",
        "W-4 | Chief Warrant Officer 4 (CW4)",
        "W-5 | Chief Warrant Officer 5 (CW5)",
        "O-1 | Second Lieutenant (2LT)",
        "O-2 | First Lieutenant (1LT)",
        "O-3 | Captain (CPT)",
        "O-4 | Major (MAJ)",
        "O-5 | Lieutenant Colonel (LTC)",
        "O-6 | Colonel (COL)",
        "O-7+ | General Officer (BG, MG, LTG, GEN)"
    ],
    "Navy": [
        "E-1 | Seaman Recruit (SR)",
        "E-2 | Seaman Apprentice (SA)",
        "E-3 | Seaman (SN) / Fireman / Airman",
        "E-4 | Petty Officer Third Class (PO3)",
        "E-5 | Petty Officer Second Class (PO2)",
        "E-6 | Petty Officer First Class (PO1)",
        "E-7 | Chief Petty Officer (CPO)",
        "E-8 | Senior Chief Petty Officer (SCPO)",
        "E-9 | Master Chief Petty Officer (MCPO)",
        "W-2 | Chief Warrant Officer 2 (CWO2)",
        "W-3 | Chief Warrant Officer 3 (CWO3)",
        "W-4 | Chief Warrant Officer 4 (CWO4)",
        "W-5 | Chief Warrant Officer 5 (CWO5)",
        "O-1 | Ensign (ENS)",
        "O-2 | Lieutenant Junior Grade (LTJG)",
        "O-3 | Lieutenant (LT)",
        "O-4 | Lieutenant Commander (LCDR)",
        "O-5 | Commander (CDR)",
        "O-6 | Captain (CAPT)",
        "O-7+ | Flag Officer / Admiral (RDML, RADM, VADM, ADM)"
    ],
    "Air Force": [
        "E-1 | Airman Basic (AB)",
        "E-2 | Airman (Amn)",
        "E-3 | Airman First Class (A1C)",
        "E-4 | Senior Airman (SrA)",
        "E-5 | Staff Sergeant (SSgt)",
        "E-6 | Technical Sergeant (TSgt)",
        "E-7 | Master Sergeant (MSgt)",
        "E-8 | Senior Master Sergeant (SMSgt)",
        "E-9 | Chief Master Sergeant (CMSgt)",
        "O-1 | Second Lieutenant (2d Lt)",
        "O-2 | First Lieutenant (1st Lt)",
        "O-3 | Captain (Capt)",
        "O-4 | Major (Maj)",
        "O-5 | Lieutenant Colonel (Lt Col)",
        "O-6 | Colonel (Col)",
        "O-7+ | General Officer (Brig Gen, Maj Gen, Lt Gen, Gen)"
    ],
    "Marine Corps": [
        "E-1 | Private (Pvt)",
        "E-2 | Private First Class (PFC)",
        "E-3 | Lance Corporal (LCpl)",
        "E-4 | Corporal (Cpl)",
        "E-5 | Sergeant (Sgt)",
        "E-6 | Staff Sergeant (SSgt)",
        "E-7 | Gunnery Sergeant (GySgt)",
        "E-8 | Master Sergeant (MSgt) / First Sergeant (1stSgt)",
        "E-9 | Master Gunnery Sergeant (MGySgt) / Sergeant Major (SgtMaj)",
        "W-1 | Warrant Officer 1 (WO1)",
        "W-2 | Chief Warrant Officer 2 (CWO2)",
        "W-3 | Chief Warrant Officer 3 (CWO3)",
        "W-4 | Chief Warrant Officer 4 (CWO4)",
        "W-5 | Chief Warrant Officer 5 (CWO5)",
        "O-1 | Second Lieutenant (2ndLt)",
        "O-2 | First Lieutenant (1stLt)",
        "O-3 | Captain (Capt)",
        "O-4 | Major (Maj)",
        "O-5 | Lieutenant Colonel (LtCol)",
        "O-6 | Colonel (Col)",
        "O-7+ | General Officer (BGen, MajGen, LtGen, Gen)"
    ],
    "Coast Guard": [
        "E-1 | Seaman Recruit (SR)",
        "E-2 | Seaman Apprentice (SA)",
        "E-3 | Seaman (SN)",
        "E-4 | Petty Officer Third Class (PO3)",
        "E-5 | Petty Officer Second Class (PO2)",
        "E-6 | Petty Officer First Class (PO1)",
        "E-7 | Chief Petty Officer (CPO)",
        "E-8 | Senior Chief Petty Officer (SCPO)",
        "E-9 | Master Chief Petty Officer (MCPO)",
        "W-2 | Chief Warrant Officer 2 (CWO2)",
        "W-3 | Chief Warrant Officer 3 (CWO3)",
        "W-4 | Chief Warrant Officer 4 (CWO4)",
        "O-1 | Ensign (ENS)",
        "O-2 | Lieutenant Junior Grade (LTJG)",
        "O-3 | Lieutenant (LT)",
        "O-4 | Lieutenant Commander (LCDR)",
        "O-5 | Commander (CDR)",
        "O-6 | Captain (CAPT)",
        "O-7+ | Admiral (RDML, RADM, VADM, ADM)"
    ],
    "Space Force": [
        "E-1 | Specialist 1 (Spc1)",
        "E-2 | Specialist 2 (Spc2)",
        "E-3 | Specialist 3 (Spc3)",
        "E-4 | Specialist 4 (Spc4)",
        "E-5 | Sergeant (Sgt)",
        "E-6 | Technical Sergeant (TSgt)",
        "E-7 | Master Sergeant (MSgt)",
        "E-8 | Senior Master Sergeant (SMSgt)",
        "E-9 | Chief Master Sergeant (CMSgt)",
        "O-1 | Second Lieutenant (2d Lt)",
        "O-2 | First Lieutenant (1st Lt)",
        "O-3 | Captain (Capt)",
        "O-4 | Major (Maj)",
        "O-5 | Lieutenant Colonel (Lt Col)",
        "O-6 | Colonel (Col)",
        "O-7+ | General (Brig Gen, Maj Gen, Lt Gen, Gen)"
    ]
}


# Comprehensive MOS / AFSC / Rating Database
MOS_DATABASE: Dict[str, Dict] = {
    # =========================================================================
    # ARMY - COMBAT ARMS & SPECIAL OPERATIONS
    # =========================================================================
    "11B": {
        "branch": "Army",
        "title": "Infantryman",
        "civilian_titles": ["Operations Supervisor", "Field Project Coordinator", "Physical Security Manager", "Team Lead", "Emergency Response Specialist"],
        "transferable_skills": ["team leadership", "high-stress decision making", "tactical execution", "risk assessment", "situational awareness", "operational planning", "accountability"],
        "tech_skills": ["tactical communications", "gps navigation", "sop compliance"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Leadership"
    },
    "11C": {
        "branch": "Army",
        "title": "Indirect Fire Infantryman (Mortarman)",
        "civilian_titles": ["Field Operations Lead", "Surveying & Ballistics Tech", "Safety Coordinator", "Site Supervisor"],
        "transferable_skills": ["precision calculation", "team leadership", "fire direction", "heavy equipment handling", "safety compliance"],
        "tech_skills": ["fire control systems", "ballistic computation", "digital targeting"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Operations"
    },
    "19D": {
        "branch": "Army",
        "title": "Cavalry Scout",
        "civilian_titles": ["Reconnaissance & Field Operations Lead", "Surveillance Specialist", "Logistics Coordinator", "Security Consultant"],
        "transferable_skills": ["reconnaissance", "threat identification", "terrain analysis", "rapid communication", "situational reporting"],
        "tech_skills": ["thermal optics", "digital battle tracking", "tactical radios"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Operations"
    },
    "19K": {
        "branch": "Army",
        "title": "M1 Armor Crewman (Tanker)",
        "civilian_titles": ["Heavy Equipment Operations Lead", "Maintenance Supervisor", "Fleet Coordinator", "Field Technician"],
        "transferable_skills": ["heavy armor operations", "preventive maintenance", "crew coordination", "fire control", "tactical mobility"],
        "tech_skills": ["hydraulic systems", "fire control computers", "power generation"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Operations"
    },
    "12B": {
        "branch": "Army",
        "title": "Combat Engineer",
        "civilian_titles": ["Construction Project Manager", "Demolition & Site Prep Lead", "Field Safety Inspector", "Civil Infrastructure Lead"],
        "transferable_skills": ["structural breaching", "demolition safety", "route clearance", "construction management", "heavy machinery operations"],
        "tech_skills": ["cad blueprints", "explosives handling", "heavy machinery", "structural modeling"],
        "typical_clearance": "Secret",
        "category": "Engineering & Construction"
    },
    "13B": {
        "branch": "Army",
        "title": "Cannon Crewmember (Field Artillery)",
        "civilian_titles": ["Industrial Machinery Operator", "Field Production Supervisor", "Safety & Compliance Lead", "Operations Team Leader"],
        "transferable_skills": ["precision artillery operations", "heavy weapon maintenance", "crew leadership", "safety enforcement", "standard operating procedures"],
        "tech_skills": ["fire direction systems", "heavy machinery", "hydraulics"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Operations"
    },
    "13F": {
        "branch": "Army",
        "title": "Joint Fire Support Specialist (Forward Observer)",
        "civilian_titles": ["Targeting & GIS Analyst", "Field Operations Coordinator", "Airspace & Drone Coordinator", "Liaison Officer"],
        "transferable_skills": ["target acquisition", "air-to-ground coordination", "geospatial mapping", "high-tempo communications", "precision coordinates"],
        "tech_skills": ["gis mapping", "laser rangefinders", "digital targeting software", "radios"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Intelligence"
    },
    "18Z": {
        "branch": "Army",
        "title": "Special Forces Senior Sergeant / Operations Team Sergeant",
        "civilian_titles": ["Director of Operations", "Senior Solutions Architect", "Enterprise Program Manager", "Chief of Staff", "VP of Operations"],
        "transferable_skills": ["executive leadership", "strategic planning", "crisis management", "cross-functional operations", "risk assessment", "mission planning", "stakeholder management"],
        "tech_skills": ["data analytics", "satellite communications", "command & control systems", "operations research"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Special Operations & Executive Leadership"
    },
    "18F": {
        "branch": "Army",
        "title": "Special Forces Assistant Operations and Intelligence Sergeant",
        "civilian_titles": ["Intelligence Operations Lead", "Threat Intelligence Architect", "Solutions Architect", "Data Analytics Lead"],
        "transferable_skills": ["intelligence analysis", "link analysis", "executive data briefings", "threat modeling", "inter-agency coordination", "OPSEC", "risk mitigation"],
        "tech_skills": ["palantir", "i2 analyst notebook", "python", "data pipelines", "geospatial intelligence", "sql"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Special Operations & Intelligence"
    },
    "18E": {
        "branch": "Army",
        "title": "Special Forces Communications Sergeant",
        "civilian_titles": ["Telecommunications Engineer", "Network Architect", "Systems Administrator", "Field Support Engineer"],
        "transferable_skills": ["tactical communications", "troubleshooting", "satellite systems", "hardware maintenance", "field operations"],
        "tech_skills": ["rf communications", "satcom", "networking", "cisco", "cryptography", "voip", "antennas"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Special Operations & Communications"
    },
    "18D": {
        "branch": "Army",
        "title": "Special Forces Medical Sergeant",
        "civilian_titles": ["Physician Assistant (PA)", "Emergency Medical Director", "Clinical Operations Manager", "Trauma Specialist"],
        "transferable_skills": ["trauma medicine", "surgical procedures", "pharmacology", "triage", "public health assessment", "emergency response"],
        "tech_skills": ["electronic health records", "medical equipment diagnostic", "telemedicine"],
        "typical_clearance": "Secret",
        "category": "Special Operations & Medical"
    },
    "18B": {
        "branch": "Army",
        "title": "Special Forces Weapons Sergeant",
        "civilian_titles": ["Security Operations Manager", "Logistics & Armory Director", "Tactical Trainer", "Risk Consultant"],
        "transferable_skills": ["weapons systems", "tactical training", "risk management", "physical security", "instructional design"],
        "tech_skills": ["inventory management", "ballistics modeling", "security protocols"],
        "typical_clearance": "Secret",
        "category": "Special Operations & Combat"
    },
    "18C": {
        "branch": "Army",
        "title": "Special Forces Engineer Sergeant",
        "civilian_titles": ["Civil Project Manager", "Infrastructure Engineer", "Facilities Director", "Field Engineering Lead"],
        "transferable_skills": ["structural analysis", "explosives safety", "demolition", "construction management", "resource planning"],
        "tech_skills": ["cad", "structural modeling", "construction estimating", "quality control"],
        "typical_clearance": "Secret",
        "category": "Special Operations & Engineering"
    },

    # =========================================================================
    # ARMY - LOGISTICS, MAINTENANCE, TRANSPORTATION & SUPPLY
    # =========================================================================
    "88M": {
        "branch": "Army",
        "title": "Motor Transport Operator",
        "civilian_titles": ["Fleet Logistics Manager", "Commercial Driver (CDL-A)", "Transportation Dispatcher", "Distribution Supervisor", "Route Logistics Lead"],
        "transferable_skills": ["heavy vehicle operations", "route planning", "cargo safety", "preventive maintenance", "dot compliance", "convoy leadership"],
        "tech_skills": ["fleet telematics", "gps dispatch software", "inventory systems"],
        "typical_clearance": "Secret",
        "category": "Logistics & Transportation"
    },
    "92A": {
        "branch": "Army",
        "title": "Automated Logistical Specialist",
        "civilian_titles": ["Supply Chain Analyst", "Warehouse Operations Manager", "Logistics Coordinator", "Inventory Controller", "ERP Systems Specialist"],
        "transferable_skills": ["supply chain optimization", "inventory auditing", "fleet tracking", "procurement", "shipping & receiving", "warehouse management"],
        "tech_skills": ["sap", "erp software", "excel", "wms (warehouse management systems)", "sql"],
        "typical_clearance": "Secret",
        "category": "Logistics & Supply Chain"
    },
    "92Y": {
        "branch": "Army",
        "title": "Unit Supply Specialist",
        "civilian_titles": ["Property Manager", "Asset Manager", "Procurement Specialist", "Inventory Controller", "Supply Chain Supervisor"],
        "transferable_skills": ["property accountability", "asset tracking", "budget reconciliation", "vendor coordination", "audit readiness"],
        "tech_skills": ["inventory databases", "excel", "erp software", "garmy"],
        "typical_clearance": "Secret",
        "category": "Logistics & Supply Chain"
    },
    "92F": {
        "branch": "Army",
        "title": "Petroleum Supply Specialist",
        "civilian_titles": ["Fuel Distribution Manager", "Hazmat Safety Coordinator", "Refinery Operations Specialist", "Logistics Terminal Manager"],
        "transferable_skills": ["fuel storage & distribution", "hazmat compliance", "pipeline operations", "quality control testing", "environmental safety"],
        "tech_skills": ["fuel testing equipment", "metering systems", "epa/osha compliance"],
        "typical_clearance": "Secret",
        "category": "Logistics & Hazmat"
    },
    "91B": {
        "branch": "Army",
        "title": "Wheeled Vehicle Mechanic",
        "civilian_titles": ["Diesel Fleet Mechanic", "Automotive Service Technician", "Maintenance Shop Foreman", "Field Service Technician"],
        "transferable_skills": ["diesel engine overhaul", "electrical troubleshooting", "hydraulic repair", "preventive maintenance inspection", "diagnostic testing"],
        "tech_skills": ["obd diagnostics", "hydraulic schematics", "electrical multimeters", "power tools"],
        "typical_clearance": "Secret",
        "category": "Maintenance & Mechanics"
    },
    "91X": {
        "branch": "Army",
        "title": "Maintenance Supervisor / Senior Mechanic",
        "civilian_titles": ["Fleet Maintenance Director", "Plant Maintenance Supervisor", "Operations Maintenance Lead", "Equipment Manager"],
        "transferable_skills": ["fleet maintenance planning", "parts procurement", "technician supervision", "work order management", "safety compliance"],
        "tech_skills": ["cmms software", "erp", "diagnostic tooling"],
        "typical_clearance": "Secret",
        "category": "Maintenance & Mechanics"
    },
    "15T": {
        "branch": "Army",
        "title": "UH-60 Black Hawk Helicopter Repairer",
        "civilian_titles": ["Aviation Maintenance Technician (A&P)", "Helicopter Technician", "Aerospace Quality Inspector", "Aviation Field Specialist"],
        "transferable_skills": ["turbine engine maintenance", "rotor systems repair", "faa/military aviation standards", "avionics troubleshooting", "flight line operations"],
        "tech_skills": ["faa airframe & powerplant standards", "avionics diagnostics", "precision torque tools"],
        "typical_clearance": "Secret",
        "category": "Aviation & Maintenance"
    },
    "15U": {
        "branch": "Army",
        "title": "CH-47 Chinook Helicopter Repairer",
        "civilian_titles": ["Heavy Lift Aviation Tech (A&P)", "Aerospace Technician", "Flight Line Supervisor", "Maintenance Lead"],
        "transferable_skills": ["heavy helicopter airframe repair", "hydraulic power systems", "drivetrain overhaul", "inspection logs"],
        "tech_skills": ["aviation technical manuals", "ndt (non-destructive testing)", "hydraulic testing"],
        "typical_clearance": "Secret",
        "category": "Aviation & Maintenance"
    },

    # =========================================================================
    # ARMY - MEDICAL, LAW ENFORCEMENT & ADMINISTRATION
    # =========================================================================
    "68W": {
        "branch": "Army",
        "title": "Combat Medic Specialist",
        "civilian_titles": ["Emergency Medical Technician (EMT / Paramedic)", "Clinical Care Specialist", "Emergency Room Tech", "Healthcare Operations Lead"],
        "transferable_skills": ["emergency trauma care", "patient triage", "vital signs assessment", "medical documentation", "critical decision making", "cpr / bls"],
        "tech_skills": ["electronic medical records (emr)", "defibrillators", "telehealth"],
        "typical_clearance": "Secret",
        "category": "Healthcare & Medical"
    },
    "68P": {
        "branch": "Army",
        "title": "Radiology Specialist",
        "civilian_titles": ["Radiologic Technologist (RT)", "X-Ray Technician", "CT / MRI Technologist", "Diagnostic Imaging Specialist"],
        "transferable_skills": ["diagnostic x-ray imaging", "radiation safety", "patient positioning", "pacs management", "dicom protocols"],
        "tech_skills": ["pacs", "dicom", "x-ray / ct scanners", "emr"],
        "typical_clearance": "Secret",
        "category": "Healthcare & Medical"
    },
    "31B": {
        "branch": "Army",
        "title": "Military Police (MP)",
        "civilian_titles": ["Police Officer / State Trooper", "Corporate Physical Security Manager", "Loss Prevention Investigator", "Security Operations Lead"],
        "transferable_skills": ["law enforcement", "access control", "criminal investigation", "conflict de-escalation", "emergency response", "evidence handling"],
        "tech_skills": ["cctv systems", "incident reporting databases", "radar / lidar"],
        "typical_clearance": "Secret",
        "category": "Law Enforcement & Security"
    },
    "31D": {
        "branch": "Army",
        "title": "CID Special Agent (Criminal Investigation)",
        "civilian_titles": ["Federal Special Agent (FBI/DEA/ATF)", "Corporate Fraud Investigator", "Forensic Investigator", "Compliance Director"],
        "transferable_skills": ["felony investigations", "forensic evidence gathering", "interrogation & interview", "case file preparation", "court testimony"],
        "tech_skills": ["digital forensics", "case management systems", "background databases"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Law Enforcement & Security"
    },
    "42A": {
        "branch": "Army",
        "title": "Human Resources Specialist",
        "civilian_titles": ["Human Resources Generalist", "HR Operations Specialist", "Talent Acquisition Coordinator", "Personnel Administrator", "Payroll Specialist"],
        "transferable_skills": ["personnel records management", "benefits administration", "onboarding / outboarding", "hr compliance", "customer service"],
        "tech_skills": ["hris (workday, peoplesoft)", "excel", "database management"],
        "typical_clearance": "Secret",
        "category": "Human Resources & Administration"
    },
    "36B": {
        "branch": "Army",
        "title": "Financial Management Technician",
        "civilian_titles": ["Financial Analyst", "Staff Accountant", "Payroll Administrator", "Accounts Payable / Receivable Lead"],
        "transferable_skills": ["budget auditing", "disbursement accounting", "financial reporting", "dfas compliance", "ledger reconciliation"],
        "tech_skills": ["sap", "excel", "accounting software", "database queries"],
        "typical_clearance": "Secret",
        "category": "Finance & Accounting"
    },

    # =========================================================================
    # ARMY - IT, CYBER, SIGNAL & INTELLIGENCE
    # =========================================================================
    "25B": {
        "branch": "Army",
        "title": "Information Technology Specialist",
        "civilian_titles": ["IT Support Specialist", "Systems Administrator", "Network Administrator", "Cloud Support Engineer", "Help Desk Lead"],
        "transferable_skills": ["hardware troubleshooting", "user support", "system configuration", "network administration", "it service management"],
        "tech_skills": ["windows server", "active directory", "cisco", "linux", "tcp/ip", "powershell", "virtualization", "dns", "dhcp", "security+"],
        "typical_clearance": "Secret",
        "category": "Information Technology"
    },
    "25U": {
        "branch": "Army",
        "title": "Signal Support Systems Specialist",
        "civilian_titles": ["Telecommunications Technician", "Field Network Technician", "Radio Communications Lead", "Systems Support Specialist"],
        "transferable_skills": ["rf communications", "satellite systems setup", "tactical radio troubleshooting", "network cabling", "voip configuration"],
        "tech_skills": ["cisco", "tactical radios (sin grain / harris)", "satcom", "fiber optics"],
        "typical_clearance": "Secret",
        "category": "Communications & IT"
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
        "title": "Human Intelligence Collector (HUMINT)",
        "civilian_titles": ["Corporate Investigator", "Talent Acquisition Specialist", "Compliance Interviewer", "Negotiation Consultant"],
        "transferable_skills": ["interpersonal interviewing", "debriefing", "source management", "cross-cultural communication", "negotiation"],
        "tech_skills": ["investigative databases", "case management systems", "foreign languages"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    },
    "35N": {
        "branch": "Army",
        "title": "Signals Intelligence Analyst (SIGINT)",
        "civilian_titles": ["Telecommunications Data Analyst", "RF Spectrum Analyst", "Cyber Threat Intelligence Analyst", "Data Engineer"],
        "transferable_skills": ["signal interception", "rf analysis", "traffic pattern analysis", "cryptologic reporting"],
        "tech_skills": ["spectrum analyzers", "python", "sql", "signal processing software"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Intelligence & Analytics"
    },

    # =========================================================================
    # NAVY - ALL RATINGS
    # =========================================================================
    "BM": {
        "branch": "Navy",
        "title": "Boatswain's Mate",
        "civilian_titles": ["Maritime Operations Supervisor", "Harbor / Port Operations Lead", "Deck Officer", "Rigging Supervisor", "Safety Lead"],
        "transferable_skills": ["maritime navigation", "deck seamanship", "crane & winch operations", "safety enforcement", "crew leadership"],
        "tech_skills": ["marine navigation systems", "rigging equipment", "preventive maintenance"],
        "typical_clearance": "Secret",
        "category": "Maritime Operations & Deck"
    },
    "HM": {
        "branch": "Navy",
        "title": "Hospital Corpsman",
        "civilian_titles": ["Clinical Nurse Assistant", "Paramedic / EMT", "Medical Operations Manager", "Surgical Technologist", "Clinic Lead"],
        "transferable_skills": ["patient assessment", "field trauma care", "surgical assisting", "preventive medicine", "medical admin"],
        "tech_skills": ["emr/ehr software", "vital monitors", "clinical lab equipment"],
        "typical_clearance": "Secret",
        "category": "Healthcare & Medical"
    },
    "IT": {
        "branch": "Navy",
        "title": "Information Systems Technician",
        "civilian_titles": ["Network Engineer", "Systems Administrator", "Cloud Support Engineer", "Cybersecurity Specialist", "IT Infrastructure Lead"],
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
    "LS": {
        "branch": "Navy",
        "title": "Logistics Specialist",
        "civilian_titles": ["Supply Chain Coordinator", "Inventory Control Specialist", "Purchasing Agent", "Warehouse Supervisor"],
        "transferable_skills": ["materials management", "inventory reconciliation", "procurement", "shipping & receiving", "budget tracking"],
        "tech_skills": ["erp", "sap", "excel", "supply databases"],
        "typical_clearance": "Secret",
        "category": "Logistics & Supply Chain"
    },
    "MA": {
        "branch": "Navy",
        "title": "Master-at-Arms (Security Forces)",
        "civilian_titles": ["Security Manager", "Law Enforcement Officer", "Anti-Terrorism Officer", "Physical Security Specialist"],
        "transferable_skills": ["force protection", "perimeter security", "k-9 operations", "incident investigation", "access control"],
        "tech_skills": ["cctv", "biometrics", "access control systems"],
        "typical_clearance": "Secret",
        "category": "Law Enforcement & Security"
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
    "MM": {
        "branch": "Navy",
        "title": "Machinist's Mate",
        "civilian_titles": ["Stationary Engineer", "Power Plant Operator", "Industrial HVAC Technician", "Mechanical Maintenance Tech"],
        "transferable_skills": ["steam propulsion", "pumps & valves overhaul", "refrigeration systems", "boiler maintenance", "troubleshooting"],
        "tech_skills": ["hydraulics", "pneumatics", "gauge calibration", "boiler systems"],
        "typical_clearance": "Secret",
        "category": "Mechanical & Plant Operations"
    },
    "CS": {
        "branch": "Navy",
        "title": "Culinary Specialist",
        "civilian_titles": ["Executive Chef / Kitchen Manager", "Food & Beverage Director", "Catering Operations Lead", "Hospitality Supervisor"],
        "transferable_skills": ["large-scale food preparation", "inventory management", "food safety (servsafe)", "menu planning", "kitchen leadership"],
        "tech_skills": ["food management software", "inventory systems"],
        "typical_clearance": "Secret",
        "category": "Hospitality & Culinary"
    },

    # =========================================================================
    # AIR FORCE & SPACE FORCE
    # =========================================================================
    "1D7X1": {
        "branch": "Air Force",
        "title": "Cyber Defense Operations",
        "civilian_titles": ["Cloud Systems Engineer", "DevOps Engineer", "Network Infrastructure Lead", "Cyber Operations Analyst"],
        "transferable_skills": ["enterprise network operations", "server virtualization", "cloud migration", "cyber defense", "incident remediation"],
        "tech_skills": ["aws", "azure", "kubernetes", "cisco", "linux", "windows server", "python", "ansible", "security+"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Information Technology & Cloud"
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
    "3P0X1": {
        "branch": "Air Force",
        "title": "Security Forces",
        "civilian_titles": ["Airfield Security Manager", "Police Officer", "Physical Security Consultant", "Emergency Services Lead"],
        "transferable_skills": ["base defense", "flight line security", "law enforcement", "anti-terrorism", "active shooter response"],
        "tech_skills": ["surveillance systems", "access control", "tactical weapons"],
        "typical_clearance": "Secret",
        "category": "Law Enforcement & Security"
    },
    "2T2X1": {
        "branch": "Air Force",
        "title": "Air Transportation Specialist (Air Mobility)",
        "civilian_titles": ["Air Cargo Operations Manager", "Airport Ramp Operations Supervisor", "Logistics & Freight Coordinator", "Hazardous Material Cargo Inspector"],
        "transferable_skills": ["air cargo loading/rigging", "aircraft weight & balance", "hazmat air transport", "fleet scheduling", "ramp safety"],
        "tech_skills": ["cargo manifesting systems", "weight & balance computers", "forklifts"],
        "typical_clearance": "Secret",
        "category": "Logistics & Aviation"
    },
    "2A6X1": {
        "branch": "Air Force",
        "title": "Aerospace Propulsion (Jet Engine Mechanic)",
        "civilian_titles": ["Jet Engine Overhaul Technician", "Aerospace Powerplant Mechanic", "Turbine Field Service Engineer", "Aviation Quality Inspector"],
        "transferable_skills": ["jet engine test cell ops", "turbine teardown & rebuild", "boroscope inspection", "faa powerplant standards"],
        "tech_skills": ["boroscopes", "engine diagnostic test sets", "precision measurement"],
        "typical_clearance": "Secret",
        "category": "Aviation & Maintenance"
    },
    "4N0X1": {
        "branch": "Air Force",
        "title": "Aerospace Medical Service",
        "civilian_titles": ["Flight Paramedic / EMT", "Emergency Room Technician", "Clinical Supervisor", "Healthcare Administrator"],
        "transferable_skills": ["flight medicine triage", "emergency clinical care", "in-flight patient care", "medical records", "immunization clinics"],
        "tech_skills": ["emr", "ventilators", "vital monitors", "aero-medical transport gear"],
        "typical_clearance": "Secret",
        "category": "Healthcare & Medical"
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
    "5S0X1": {
        "branch": "Space Force",
        "title": "Space Operations Specialist",
        "civilian_titles": ["Satellite Orbital Controller", "Space Domain Awareness Analyst", "Telemetry & Tracking Specialist"],
        "transferable_skills": ["satellite orbit determination", "spacecraft commanding", "missile warning tracking", "sensor network ops"],
        "tech_skills": ["astrodynamics software", "orbital telemetry", "radar tracking"],
        "typical_clearance": "Top Secret / SCI",
        "category": "Space & Operations"
    },

    # =========================================================================
    # MARINE CORPS - ALL FIELDS
    # =========================================================================
    "0311": {
        "branch": "Marine Corps",
        "title": "Rifleman",
        "civilian_titles": ["Operations Supervisor", "Field Logistics Coordinator", "Physical Security Specialist", "Team Leader"],
        "transferable_skills": ["discipline", "leadership in ambiguity", "high-tempo execution", "situational awareness", "team cohesion"],
        "tech_skills": ["tactical radio systems", "sop compliance", "risk assessment"],
        "typical_clearance": "Secret",
        "category": "Combat Arms & Leadership"
    },
    "0671": {
        "branch": "Marine Corps",
        "title": "Data Systems Administrator",
        "civilian_titles": ["Systems Administrator", "Cloud Infrastructure Engineer", "IT Operations Lead", "DevOps Specialist"],
        "transferable_skills": ["expeditionary server deployment", "virtualization", "system recovery", "directory services", "tactical networks"],
        "tech_skills": ["vmware", "active directory", "windows server", "linux", "cisco", "powershell", "san"],
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
    "0431": {
        "branch": "Marine Corps",
        "title": "Logistics / Embarkation Specialist",
        "civilian_titles": ["Intermodal Logistics Manager", "Freight Operations Lead", "Supply Chain Distribution Lead", "Port Operations Coordinator"],
        "transferable_skills": ["deployment logistics", "cargo load planning", "air/sea/rail transport coordination", "customs & hazmat manifesting"],
        "tech_skills": ["icodes", "logistics software", "load optimization"],
        "typical_clearance": "Secret",
        "category": "Logistics & Supply Chain"
    },
    "3531": {
        "branch": "Marine Corps",
        "title": "Motor Vehicle Operator",
        "civilian_titles": ["Fleet Transport Lead", "Commercial Driver (CDL-A)", "Heavy Equipment Operator", "Logistics Dispatcher"],
        "transferable_skills": ["tactical truck driving", "convoy safety", "off-road recovery", "cargo securing", "preventive maintenance"],
        "tech_skills": ["telematics", "vehicle maintenance logs"],
        "typical_clearance": "Secret",
        "category": "Logistics & Transportation"
    },
    "5811": {
        "branch": "Marine Corps",
        "title": "Military Police",
        "civilian_titles": ["Law Enforcement Officer", "Corporate Security Director", "Access Control Specialist", "Emergency Operations Lead"],
        "transferable_skills": ["crime prevention", "tactical response", "access control", "investigations", "conflict resolution"],
        "tech_skills": ["cctv", "biometrics", "incident reporting"],
        "typical_clearance": "Secret",
        "category": "Law Enforcement & Security"
    },

    # =========================================================================
    # COAST GUARD - ALL RATINGS
    # =========================================================================
    "ME": {
        "branch": "Coast Guard",
        "title": "Maritime Enforcement Specialist",
        "civilian_titles": ["Federal Law Enforcement Agent (CBP/ICE)", "Maritime Security Officer", "Anti-Terrorism Specialist", "Port Security Lead"],
        "transferable_skills": ["maritime boarding operations", "counter-narcotics", "tactical boat operations", "physical security", "law enforcement"],
        "tech_skills": ["boarding software", "tactical gear", "cctv"],
        "typical_clearance": "Secret",
        "category": "Law Enforcement & Security"
    },
    "MK": {
        "branch": "Coast Guard",
        "title": "Machinery Technician",
        "civilian_titles": ["Marine Diesel Mechanic", "Industrial Machinery Technician", "Power Generation Lead", "HVAC / Hydraulics Specialist"],
        "transferable_skills": ["marine diesel overhaul", "hydraulic and pneumatic maintenance", "auxiliary machinery repair", "damage control"],
        "tech_skills": ["marine diesel engines", "hydraulics", "electrical systems"],
        "typical_clearance": "Secret",
        "category": "Maintenance & Mechanics"
    },
    "MST": {
        "branch": "Coast Guard",
        "title": "Marine Science Technician",
        "civilian_titles": ["Environmental Health & Safety (EHS) Manager", "Pollution Response Specialist", "Port Safety Inspector", "Regulatory Compliance Officer"],
        "transferable_skills": ["oil spill response", "hazmat container inspection", "environmental compliance", "facility audits", "incident command"],
        "tech_skills": ["hazmat databases", "gis", "environmental monitoring sets"],
        "typical_clearance": "Secret",
        "category": "Environmental & Safety"
    }
}


def lookup_mos(query: str) -> Optional[Dict]:
    """
    Look up an MOS code or search by keyword across all military specialties.
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
    
    # Strip common prefixes (e.g., "MOS 11B" -> "11B", "AFSC 1D7X1" -> "1D7X1")
    for word in clean_query.split():
        if word in MOS_DATABASE:
            result = MOS_DATABASE[word].copy()
            result["code"] = word
            return result
            
    # Fuzzy search on title, category, or transferable skills
    query_lower = query.lower()
    for code, data in MOS_DATABASE.items():
        if (query_lower in data["title"].lower() or 
            query_lower in data.get("category", "").lower() or 
            any(query_lower in s.lower() for s in data["transferable_skills"]) or
            any(query_lower in ct.lower() for ct in data["civilian_titles"])):
            result = data.copy()
            result["code"] = code
            return result
            
    return None


def get_mos_choices_by_branch(branch: str = "All") -> List[str]:
    """Get list of formatted MOS choices filtered by branch"""
    choices = []
    for code, data in MOS_DATABASE.items():
        if branch == "All" or data["branch"].lower() == branch.lower():
            choices.append(f"{code} - {data['title']} ({data['branch']})")
    return sorted(choices)
