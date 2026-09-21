import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from app.config.settings import settings

def generate_pdf_report(report_data: Dict[str, Any], workspace_id: str) -> str:
    """Generate a high-quality executive business report PDF with professional layout."""
    workspace_dir = os.path.join(settings.STORAGE_PATH, str(workspace_id), "reports")
    os.makedirs(workspace_dir, exist_ok=True)
    
    filename = f"report_{uuid.uuid4().hex[:12]}.pdf"
    file_path = os.path.join(workspace_dir, filename)
    
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#4F46E5") # Indigo
    dark_color = colors.HexColor("#1E293B")    # Slate 800
    gray_color = colors.HexColor("#64748B")    # Slate 500
    light_bg = colors.HexColor("#F8FAFC")      # Slate 50
    border_color = colors.HexColor("#E2E8F0")  # Slate 200
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=gray_color
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=dark_color,
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=dark_color
    )
    
    story = []
    
    # 1. Header Banner
    story.append(Paragraph("DataPilot AI — Executive Report", title_style))
    title_text = report_data.get("title", "Dataset Analysis & Business Insights")
    dataset_name = report_data.get("dataset_name", "Dataset")
    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    
    story.append(Paragraph(f"<b>Title:</b> {title_text} &nbsp;|&nbsp; <b>Dataset:</b> {dataset_name} &nbsp;|&nbsp; <b>Generated:</b> {date_str}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=15))
    
    # 2. Executive Summary
    story.append(Paragraph("Executive Summary", h2_style))
    analysis = report_data.get("analysis", {})
    summary = analysis.get("summary", {})
    dataset_type = report_data.get("dataset_type", "General Analytics")
    quality_score = report_data.get("quality_score", 90.0)
    
    summary_text = (
        f"This report presents an automated intelligence analysis for the <b>{dataset_name}</b> "
        f"({dataset_type} dataset). The data contains {summary.get('rows', 'N/A')} records across "
        f"{summary.get('columns', 'N/A')} attributes. Automated profiling and data cleaning routines were "
        f"applied, achieving a composite data quality rating of <b>{quality_score:.1f}/100</b>."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 12))
    
    # 3. Key Performance Indicators (KPIs)
    kpis = analysis.get("kpis", [])
    if kpis:
        story.append(Paragraph("Key Performance Indicators (KPIs)", h2_style))
        kpi_table_data = [["Metric", "Value", "Description"]]
        for k in kpis:
            name = k.get("name", "")
            val = k.get("formatted_value") or str(k.get("value", ""))
            desc = k.get("description", "")
            kpi_table_data.append([
                Paragraph(f"<b>{name}</b>", body_style),
                Paragraph(f"<b>{val}</b>", body_style),
                Paragraph(desc, body_style)
            ])
            
        kpi_table = Table(kpi_table_data, colWidths=[140, 100, 290])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 14))
    
    # 4. Key Findings & Insights
    insights = report_data.get("insights", [])
    if insights:
        story.append(Paragraph("Key Findings & Recommendations", h2_style))
        for idx, ins in enumerate(insights[:6], 1):
            title = ins.get("title", f"Insight #{idx}")
            desc = ins.get("description", "")
            rec = ins.get("recommendation", "")
            category = ins.get("category", "General").title()
            severity = ins.get("severity", "Info").title()
            
            card_content = [
                [Paragraph(f"<b>{idx}. {title}</b> [{category} - {severity}]", body_style)],
                [Paragraph(f"<b>Observation:</b> {desc}", body_style)]
            ]
            if rec:
                card_content.append([Paragraph(f"<b>Recommendation:</b> {rec}", body_style)])
                
            ins_table = Table(card_content, colWidths=[530])
            ins_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), light_bg),
                ('BOX', (0, 0), (-1, -1), 1, border_color),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(ins_table)
            story.append(Spacer(1, 6))
            
    # 5. Methodology & Governance Footer
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceAfter=10))
    methodology_text = (
        "<i>Methodology Notice: Calculated deterministically using pandas and scikit-learn analytics engines. "
        "AI reasoning explanations are anchored to verified mathematical facts. Generated by DataPilot AI.</i>"
    )
    story.append(Paragraph(methodology_text, subtitle_style))
    
    doc.build(story)
    # Return relative storage path
    return f"{workspace_id}/reports/{filename}"
