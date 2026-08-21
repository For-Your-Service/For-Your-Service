"""
PDF Transition Brief & Tailored Civilian Resume Generator
For Your Service - 7 Eagle Group
Generates a downloadable PDF Transition Intelligence Brief and Executive Resume
for transitioning military service members and defense employers.
"""

import io
from datetime import datetime
from typing import Dict, List, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


def generate_veteran_transition_pdf(
    candidate_info: Dict[str, Any],
    extracted_skills: Dict[str, Any],
    matches: List[Dict[str, Any]],
    readiness: Dict[str, Any],
    mos_info: Dict[str, Any]
) -> bytes:
    """
    Generate a complete, executive-grade PDF Transition Intelligence Brief & Resume.
    Returns bytes suitable for Streamlit st.download_button.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette (7 Eagle Group / Defense theme)
    PRIMARY = colors.HexColor("#0b2545")    # Deep Navy
    SECONDARY = colors.HexColor("#134074")  # Slate Blue
    ACCENT = colors.HexColor("#d4af37")     # Military Gold
    TEXT_DARK = colors.HexColor("#1e293b")  # Dark Slate
    MUTED = colors.HexColor("#64748b")      # Muted Slate
    BG_LIGHT = colors.HexColor("#f8fafc")   # Off-white / light gray
    BORDER_COLOR = colors.HexColor("#cbd5e1")
    SUCCESS_COLOR = colors.HexColor("#166534")

    # Typography Styles
    style_header_title = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=TA_CENTER
    )

    style_header_subtitle = ParagraphStyle(
        "HeaderSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=ACCENT,
        alignment=TA_CENTER
    )

    style_contact_line = ParagraphStyle(
        "ContactLine",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=MUTED,
        alignment=TA_CENTER
    )

    style_section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=4
    )

    style_body = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=TEXT_DARK,
        alignment=TA_LEFT
    )

    style_bold_label = ParagraphStyle(
        "BoldLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY
    )

    story = []

    # -------------------------------------------------------------------------
    # 1. HEADER & BRANDING
    # -------------------------------------------------------------------------
    name = str(candidate_info.get("name", "Transitioning Service Member")).upper()
    branch = candidate_info.get("branch", "U.S. Military")
    rank = candidate_info.get("rank", "Veteran")
    mos_code = candidate_info.get("mos", "N/A")
    mos_title = mos_info.get("title", "Specialist") if mos_info else "Military Leader"
    clearance = candidate_info.get("clearance", "None")
    city = candidate_info.get("target_city", "")
    state = candidate_info.get("target_state", "")
    email = candidate_info.get("email", "")
    phone = candidate_info.get("phone", "")
    track = candidate_info.get("target_track", "Enterprise Technology")

    story.append(Paragraph(f"<b>{name}</b>", style_header_title))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"FOR YOUR SERVICE &bull; 7 EAGLE GROUP VETERAN CAREER BRIEF", style_header_subtitle))
    story.append(Spacer(1, 4))

    contact_parts = []
    if city and state:
        contact_parts.append(f"📍 {city.title()}, {state.upper()}")
    if phone:
        contact_parts.append(f"📞 {phone}")
    if email:
        contact_parts.append(f"✉️ {email}")
    contact_parts.append(f"🛡️ Clearance: <b>{clearance}</b>")
    contact_parts.append(f"🎖️ {branch} ({mos_code} &bull; {rank})")

    story.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_parts), style_contact_line))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=8, spaceBefore=4))

    # -------------------------------------------------------------------------
    # 2. PROFILE & TARGET OVERVIEW METRICS TABLE
    # -------------------------------------------------------------------------
    profile_table_data = [
        [
            Paragraph("<b>Target Industry Track:</b>", style_bold_label),
            Paragraph(f"<b>{track}</b>", style_body),
            Paragraph("<b>Security Clearance:</b>", style_bold_label),
            Paragraph(f"<b>{clearance}</b>", style_body)
        ],
        [
            Paragraph("<b>Military Specialty:</b>", style_bold_label),
            Paragraph(f"{mos_code} &mdash; {mos_title}", style_body),
            Paragraph("<b>Target Location:</b>", style_bold_label),
            Paragraph(f"{city.title()}, {state.upper()} ({candidate_info.get('target_radius', '50 miles')})", style_body)
        ],
        [
            Paragraph("<b>Target Compensation:</b>", style_bold_label),
            Paragraph(f"${candidate_info.get('salary_min', 80000):,.0f} - ${candidate_info.get('salary_max', 150000):,.0f}/yr", style_body),
            Paragraph("<b>Report Date:</b>", style_bold_label),
            Paragraph(f"{datetime.now().strftime('%B %d, %Y')}", style_body)
        ]
    ]

    p_table = Table(profile_table_data, colWidths=[1.8*inch, 2.2*inch, 1.6*inch, 1.8*inch])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 3. VERIFIED CORE COMPETENCIES & TECHNICAL STACK
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>🛠️ VERIFIED COMPETENCIES & TECHNICAL TOOLSET</b>", style_section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=6, spaceBefore=2))

    tech_skills = extracted_skills.get("technical_skills", [])
    lead_skills = extracted_skills.get("leadership_skills", [])
    ops_skills = extracted_skills.get("ops_skills", [])
    mos_skills = extracted_skills.get("mos_skills", [])

    all_verified = tech_skills + lead_skills + ops_skills + mos_skills
    if all_verified:
        skill_text = ", ".join([f"<b>{s.upper()}</b>" for s in all_verified[:24]])
        story.append(Paragraph(f"• <b>Technical & Operational Stack:</b> {skill_text}", style_body))
    else:
        story.append(Paragraph("• Cross-functional leadership, operational risk mitigation, team accountability, and mission planning.", style_body))

    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 4. TOP MATCHED CAREER OPPORTUNITIES
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>💼 TOP RANKED CAREER MATCHES & PARTNER EMPLOYERS</b>", style_section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=6, spaceBefore=2))

    job_rows = [
        [
            Paragraph("<b>#</b>", style_bold_label),
            Paragraph("<b>Role Title & Employer</b>", style_bold_label),
            Paragraph("<b>Location & Clearance</b>", style_bold_label),
            Paragraph("<b>Salary Range</b>", style_bold_label),
            Paragraph("<b>Fit Score</b>", style_bold_label)
        ]
    ]

    for idx, j in enumerate(matches[:5], 1):
        title = j.get("title", "Role Title")
        company = j.get("company", "Employer")
        loc = j.get("location_display", "Location")
        sal = f"${j.get('salary_min', 0):,.0f} - ${j.get('salary_max', 0):,.0f}"
        score = f"{j.get('match_score', 0):.0f}%"
        clr_req = j.get("clearance_required", "None")

        job_rows.append([
            Paragraph(f"<b>#{idx}</b>", style_body),
            Paragraph(f"<b>{title}</b><br/><font color='#64748b'>{company}</font>", style_body),
            Paragraph(f"{loc}<br/><font color='#0369a1'>🛡️ {clr_req}</font>", style_body),
            Paragraph(sal, style_body),
            Paragraph(f"<b><font color='#166534'>{score}</font></b>", style_bold_label)
        ])

    j_table = Table(job_rows, colWidths=[0.4*inch, 2.8*inch, 2.0*inch, 1.4*inch, 0.8*inch])
    j_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    # Fix header text colors for PDF Table
    for c_idx in range(5):
        j_table.setStyle(TableStyle([('TEXTCOLOR', (c_idx, 0), (c_idx, 0), colors.white)]))

    story.append(j_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 5. CAREER READINESS & RECOMMENDED FUNDED CERTIFICATIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("<b>🎓 CAREER READINESS & FREE FUNDED VETERAN CREDENTIALS</b>", style_section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=6, spaceBefore=2))

    cert_list = readiness.get("recommended_certs", [])
    if cert_list:
        for c in cert_list[:3]:
            cert_name = c.get("name", "Certification")
            cert_provider = c.get("provider", "Authorized Provider")
            cert_uplift = c.get("score_uplift", 5)
            cert_salary = c.get("salary_uplift", 15000)
            cert_link = c.get("link", "#")

            cert_text = f"• <b>{cert_name}</b> ({cert_provider}) &mdash; Projected Uplift: <b>+{cert_uplift}% Match</b> (+${cert_salary:,}/yr). <i>Free Veteran Funding: Onward to Opportunity (O2O) / SkillBridge.</i>"
            story.append(Paragraph(cert_text, style_body))
            story.append(Spacer(1, 3))
    else:
        story.append(Paragraph("• Candidate shows strong direct alignment across core career benchmarks.", style_body))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 6. FOOTER & 7 EAGLE GROUP ATTRIBUTION
    # -------------------------------------------------------------------------
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=6, spaceBefore=6))
    footer_text = (
        "<b>7 Eagle Group Veteran Placement Platform</b> &bull; Confidential Transition Report &bull; "
        "Visit: <b>7eagle.com</b> &bull; GitHub: <b>github.com/For-Your-Service/For-Your-Service</b>"
    )
    story.append(Paragraph(footer_text, style_contact_line))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
