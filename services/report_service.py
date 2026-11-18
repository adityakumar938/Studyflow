from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from services.planner_service import PlannerService

class ReportService:
    def __init__(self, syllabus_path: str, pyq_path: str):
        self.planner = PlannerService(syllabus_path, pyq_path)

    def generate_pdf_report(self, filename: str = "study_plan_report.pdf", total_hours: int = 25):
        plan = self.planner.generate_study_plan(total_study_hours=total_hours)
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=10,
            alignment=1
        )
        elements.append(Paragraph("Study Flow - Data-Driven Study Plan", title_style))
        elements.append(Spacer(1, 10))
        
        sub_style = ParagraphStyle(
            'SubStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=20,
            alignment=1
        )
        elements.append(Paragraph(f"Total Allocated Hours: {total_hours} Hours | Syllabus-PYQ Proportional Mapping", sub_style))
        elements.append(Spacer(1, 10))
        
        table_data = [["Unit Name", "PYQ Questions", "Weightage (%)", "Recommended (Hrs)"]]
        
        for unit, details in plan.items():
            if isinstance(details, dict):
                table_data.append([
                    unit,
                    str(details.get("questions_appeared", 0)),
                    f"{details.get('weightage_percentage', 0)}%",
                    str(details.get("recommended_hours", 0))
                ])
                
        t = Table(table_data, colWidths=[210, 90, 90, 95])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#EDF2F7")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 10),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
            ('TOPPADDING', (0,1), (-1,-1), 6),
        ]))
        
        elements.append(t)
        doc.build(elements)
        return filename
