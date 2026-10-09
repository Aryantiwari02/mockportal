import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _get_styles():
    styles = getSampleStyleSheet()

    header_title = ParagraphStyle(
        "GovHeaderTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1,  # Center
    )

    header_sub = ParagraphStyle(
        "GovHeaderSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569"),
        alignment=1,
    )

    demo_badge = ParagraphStyle(
        "DemoBadge",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#b91c1c"),
        alignment=1,
    )

    section_heading = ParagraphStyle(
        "GovSectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=4,
    )

    label_style = ParagraphStyle(
        "GovLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )

    value_style = ParagraphStyle(
        "GovValue",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
    )

    table_header = ParagraphStyle(
        "GovTableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white,
    )

    declaration_text = ParagraphStyle(
        "GovDeclaration",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155"),
    )

    return {
        "styles": styles,
        "header_title": header_title,
        "header_sub": header_sub,
        "demo_badge": demo_badge,
        "section_heading": section_heading,
        "label": label_style,
        "value": value_style,
        "table_header": table_header,
        "declaration": declaration_text,
    }


def generate_application_pdf(application):
    """
    Generate an official government-style printable PDF application form
    using actual submitted application data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    st = _get_styles()
    elements = []

    # Government Header
    elements.append(Paragraph("YOJANASAATHI • SARKAR YOJANA SEVA", st["header_title"]))
    elements.append(Paragraph("Unified National Welfare & Scheme Application Portal", st["header_sub"]))
    elements.append(Paragraph("Demonstration / Mock Review Copy • Not for Official Government Submission", st["demo_badge"]))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=10))

    # Application Meta Box
    submitted_date_str = (
        application.submitted_at.strftime("%d %b %Y, %I:%M %p")
        if application.submitted_at
        else application.created_at.strftime("%d %b %Y, %I:%M %p")
    )

    meta_data = [
        [
            Paragraph("<b>Application Number:</b>", st["label"]),
            Paragraph(f"<font color='#1e3a8a'><b>{application.application_number}</b></font>", st["value"]),
            Paragraph("<b>Current Status:</b>", st["label"]),
            Paragraph(f"<b>{application.status.replace('_', ' ')}</b>", st["value"]),
        ],
        [
            Paragraph("<b>Scheme Name:</b>", st["label"]),
            Paragraph(application.scheme.title, st["value"]),
            Paragraph("<b>Scheme Category:</b>", st["label"]),
            Paragraph(application.scheme.category, st["value"]),
        ],
        [
            Paragraph("<b>Date of Application:</b>", st["label"]),
            Paragraph(submitted_date_str, st["value"]),
            Paragraph("<b>Citizen Mobile:</b>", st["label"]),
            Paragraph(f"+91 {application.citizen.mobile}", st["value"]),
        ],
    ]

    meta_table = Table(meta_data, colWidths=[110, 160, 110, 140])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 10))

    # Section 1: Applicant Details
    elements.append(Paragraph("1. APPLICANT IDENTIFICATION", st["section_heading"]))
    citizen = application.citizen
    full_name = citizen.full_name or application.form_data.get("full_name") or application.form_data.get("applicant_name") or "Registered Citizen"
    
    applicant_data = [
        [
            Paragraph("<b>Applicant Name:</b>", st["label"]),
            Paragraph(str(full_name), st["value"]),
            Paragraph("<b>Registered Mobile:</b>", st["label"]),
            Paragraph(f"+91 {citizen.mobile}", st["value"]),
        ],
        [
            Paragraph("<b>Email:</b>", st["label"]),
            Paragraph(str(citizen.email or application.form_data.get("email") or "Not Provided"), st["value"]),
            Paragraph("<b>Mobile Verification:</b>", st["label"]),
            Paragraph("<font color='#16a34a'><b>Verified via OTP</b></font>" if citizen.is_verified else "Pending", st["value"]),
        ],
        [
            Paragraph("<b>Address:</b>", st["label"]),
            Paragraph(str(citizen.address or application.form_data.get("address") or "As per uploaded documents"), st["value"]),
            Paragraph("", st["label"]),
            Paragraph("", st["value"]),
        ]
    ]

    applicant_table = Table(applicant_data, colWidths=[110, 160, 110, 140])
    applicant_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("SPAN", (1, 2), (3, 2)),
    ]))
    elements.append(applicant_table)
    elements.append(Spacer(1, 10))

    # Section 2: Scheme Form Fields
    elements.append(Paragraph("2. SCHEME APPLICATION PARTICULARS", st["section_heading"]))
    
    # Match scheme application_fields
    fields_dict = application.form_data or {}
    scheme_fields = application.scheme.application_fields or []
    field_labels = {f["name"]: f.get("label", f["name"]) for f in scheme_fields if isinstance(f, dict)}

    form_rows = []
    items_to_render = []
    for k, v in fields_dict.items():
        if k in ["declaration_consent"]:
            continue
        label = field_labels.get(k, k.replace("_", " ").title())
        display_val = "Yes" if v is True else ("No" if v is False else str(v))
        items_to_render.append((label, display_val))

    if not items_to_render:
        items_to_render.append(("Application Form", "Submitted with standard verified citizen credentials"))

    # Pair into 2 columns if possible
    i = 0
    while i < len(items_to_render):
        item1 = items_to_render[i]
        if i + 1 < len(items_to_render):
            item2 = items_to_render[i + 1]
            form_rows.append([
                Paragraph(f"<b>{item1[0]}:</b>", st["label"]),
                Paragraph(item1[1], st["value"]),
                Paragraph(f"<b>{item2[0]}:</b>", st["label"]),
                Paragraph(item2[1], st["value"]),
            ])
            i += 2
        else:
            form_rows.append([
                Paragraph(f"<b>{item1[0]}:</b>", st["label"]),
                Paragraph(item1[1], st["value"]),
                Paragraph("", st["label"]),
                Paragraph("", st["value"]),
            ])
            i += 1

    form_table = Table(form_rows, colWidths=[110, 160, 110, 140])
    form_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(form_table)
    elements.append(Spacer(1, 10))

    # Section 3: Document Verification Checklist
    elements.append(Paragraph("3. DOCUMENT UPLOAD & VERIFICATION STATUS", st["section_heading"]))
    
    doc_table_data = [
        [
            Paragraph("<b>Document Type</b>", st["table_header"]),
            Paragraph("<b>File Name</b>", st["table_header"]),
            Paragraph("<b>Upload Date</b>", st["table_header"]),
            Paragraph("<b>Verification Status</b>", st["table_header"]),
        ]
    ]

    uploaded_docs = {d.document_type: d for d in application.documents.all()}
    scheme_docs = application.scheme.documents or []
    
    # Combine required docs with uploaded docs
    all_doc_names = list(dict.fromkeys(list(scheme_docs) + list(uploaded_docs.keys())))

    for d_name in all_doc_names:
        doc_obj = uploaded_docs.get(d_name)
        if doc_obj:
            fname = doc_obj.file_name or "Uploaded"
            u_date = doc_obj.uploaded_at.strftime("%d %b %Y")
            v_status = doc_obj.verification_status
            if v_status == "VERIFIED":
                status_p = Paragraph("<font color='#16a34a'><b>✓ Verified (Demo)</b></font>", st["value"])
            elif v_status == "REJECTED":
                status_p = Paragraph("<font color='#dc2626'><b>✗ Rejected</b></font>", st["value"])
            elif v_status == "CORRECTION_REQUIRED":
                status_p = Paragraph("<font color='#d97706'><b>Correction Req.</b></font>", st["value"])
            else:
                status_p = Paragraph("<font color='#2563eb'><b>Under Review</b></font>", st["value"])
        else:
            fname = "Not Uploaded"
            u_date = "-"
            status_p = Paragraph("<font color='#94a3b8'>Pending</font>", st["value"])

        doc_table_data.append([
            Paragraph(d_name, st["value"]),
            Paragraph(fname[:30], st["value"]),
            Paragraph(u_date, st["value"]),
            status_p,
        ])

    doc_table = Table(doc_table_data, colWidths=[170, 150, 90, 110])
    doc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    elements.append(doc_table)
    elements.append(Spacer(1, 10))

    # Section 4: Declaration & Signature
    decl_block = []
    decl_block.append(Paragraph("4. STATUTORY DECLARATION & ACKNOWLEDGEMENT", st["section_heading"]))
    decl_text = (
        "I hereby solemnly declare that all information and particulars stated in this application are true, "
        "accurate, and complete to the best of my knowledge and belief. I have uploaded genuine copies of all required "
        "supporting documents. I acknowledge that this portal is a demonstration mock system and any verification "
        "performed herein represents simulated workflow verification."
    )
    decl_block.append(Paragraph(decl_text, st["declaration"]))
    decl_block.append(Spacer(1, 15))

    sig_data = [
        [
            Paragraph(f"<b>Application Date:</b> {submitted_date_str[:11]}", st["value"]),
            Paragraph("<b>Applicant Signature / Thumb:</b> ___________________", st["value"]),
        ],
        [
            Paragraph("<b>Portal Authority:</b> YojanaSaathi Demo", st["value"]),
            Paragraph("<b>Verification Seal:</b> [ Simulated Review Approved ]", st["value"]),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[250, 270])
    sig_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    decl_block.append(sig_table)

    elements.append(KeepTogether(decl_block))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_blank_form_pdf(scheme):
    """
    Generate an official government-style blank printable application form
    dynamically based on the selected scheme.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    st = _get_styles()
    elements = []

    # Government Header
    elements.append(Paragraph("YOJANASAATHI • SARKAR YOJANA SEVA", st["header_title"]))
    elements.append(Paragraph("Official Scheme Application Form (Blank Printable Copy)", st["header_sub"]))
    elements.append(Paragraph("Demonstration Portal • For Physical / Offline Submission Practice", st["demo_badge"]))
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=8))

    # Scheme Banner
    scheme_data = [
        [
            Paragraph("<b>Scheme Title:</b>", st["label"]),
            Paragraph(f"<b>{scheme.title}</b>", st["value"]),
            Paragraph("<b>Category:</b>", st["label"]),
            Paragraph(scheme.category, st["value"]),
        ],
        [
            Paragraph("<b>Scheme Code:</b>", st["label"]),
            Paragraph(scheme.id.upper(), st["value"]),
            Paragraph("<b>Description:</b>", st["label"]),
            Paragraph(scheme.short_description[:100], st["value"]),
        ]
    ]
    scheme_table = Table(scheme_data, colWidths=[100, 200, 80, 140])
    scheme_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(scheme_table)
    elements.append(Spacer(1, 8))

    # Section 1: Standard Applicant Info (Blank Write-in)
    elements.append(Paragraph("SECTION A: BASIC APPLICANT DETAILS", st["section_heading"]))
    app_blank_data = [
        [
            Paragraph("Full Name: __________________________________________________", st["value"]),
            Paragraph("Gender: [ ] M  [ ] F  [ ] Other", st["value"]),
        ],
        [
            Paragraph("Date of Birth: _____ / _____ / ________", st["value"]),
            Paragraph("Mobile No: +91 ____________________", st["value"]),
        ],
        [
            Paragraph("Aadhaar / National ID No: ________________________________", st["value"]),
            Paragraph("Email (if any): _____________________", st["value"]),
        ],
        [
            Paragraph("Permanent Address: __________________________________________________________________________________", st["value"]),
            Paragraph("", st["value"]),
        ],
    ]
    app_blank_table = Table(app_blank_data, colWidths=[310, 210])
    app_blank_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("SPAN", (0, 3), (1, 3)),
    ]))
    elements.append(app_blank_table)
    elements.append(Spacer(1, 8))

    # Section 2: Scheme Specific Fields
    elements.append(Paragraph("SECTION B: SCHEME-SPECIFIC PARTICULARS", st["section_heading"]))
    scheme_fields = scheme.application_fields or []
    
    spec_rows = []
    if scheme_fields:
        for f in scheme_fields:
            if not isinstance(f, dict):
                continue
            lbl = f.get("label", f.get("name", "Field"))
            req = " (Required)" if f.get("required") else " (Optional)"
            ftype = f.get("type", "text")
            options = f.get("options", [])
            
            if ftype in ["select", "radio"] and options:
                opts_str = "    ".join([f"[ ] {opt}" for opt in options])
                spec_rows.append([
                    Paragraph(f"<b>{lbl}{req}:</b>", st["label"]),
                    Paragraph(opts_str, st["value"]),
                ])
            elif ftype == "textarea":
                spec_rows.append([
                    Paragraph(f"<b>{lbl}{req}:</b>", st["label"]),
                    Paragraph("__________________________________________________________________________________", st["value"]),
                ])
            elif ftype == "checkbox":
                spec_rows.append([
                    Paragraph(f"[ ] {lbl}", st["label"]),
                    Paragraph("Check to confirm", st["value"]),
                ])
            else:
                spec_rows.append([
                    Paragraph(f"<b>{lbl}{req}:</b>", st["label"]),
                    Paragraph("________________________________________________________", st["value"]),
                ])
    else:
        spec_rows.append([
            Paragraph("Annual Household Income:", st["label"]),
            Paragraph("₹ ________________________________", st["value"]),
        ])
        spec_rows.append([
            Paragraph("Bank Account & IFSC:", st["label"]),
            Paragraph("A/C: _______________________  IFSC: _______________________", st["value"]),
        ])

    spec_table = Table(spec_rows, colWidths=[200, 320])
    spec_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(spec_table)
    elements.append(Spacer(1, 8))

    # Section 3: Document Checklist
    elements.append(Paragraph("SECTION C: REQUIRED DOCUMENTS CHECKLIST", st["section_heading"]))
    doc_checklist_rows = [
        [
            Paragraph("<b>Document Description</b>", st["table_header"]),
            Paragraph("<b>Check if Attached</b>", st["table_header"]),
        ]
    ]

    for d in (scheme.documents or []):
        doc_checklist_rows.append([
            Paragraph(f"• {d}", st["value"]),
            Paragraph("[  ] Enclosed with application", st["value"]),
        ])

    doc_table = Table(doc_checklist_rows, colWidths=[360, 160])
    doc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(doc_table)
    elements.append(Spacer(1, 8))

    # Section 4: Declaration
    decl_block = []
    decl_block.append(Paragraph("SECTION D: DECLARATION & SIGNATURE", st["section_heading"]))
    decl_block.append(Paragraph(
        "I hereby declare that the particulars stated by me are true to the best of my knowledge and I meet the eligibility "
        "criteria for this scheme. If any information is found incorrect, my application is liable for rejection.",
        st["declaration"]
    ))
    decl_block.append(Spacer(1, 12))

    sig_data = [
        [
            Paragraph("Date: _____ / _____ / ________", st["value"]),
            Paragraph("Place: ___________________________", st["value"]),
            Paragraph("Signature of Applicant: _____________________", st["value"]),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 200])
    decl_block.append(sig_table)
    elements.append(KeepTogether(decl_block))

    doc.build(elements)
    buffer.seek(0)
    return buffer
