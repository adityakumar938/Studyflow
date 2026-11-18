from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from services.pyq_service import PYQService
from services.planner_service import PlannerService
from services.report_service import ReportService
import os

app = FastAPI(title="Study Flow API", version="1.0")

pyq_service = PYQService("syllabus.pdf", "pyq.pdf")
planner_service = PlannerService("syllabus.pdf", "pyq.pdf")
report_service = ReportService("syllabus.pdf", "pyq.pdf")

@app.get("/")
def read_root():
    return {
        "project": "Study Flow API",
        "status": "Active",
        "endpoints": ["/plan", "/weightages", "/frequencies", "/export-pdf"]
    }

@app.get("/frequencies")
def get_frequencies():
    return pyq_service.get_topic_frequencies()

@app.get("/weightages")
def get_weightages():
    return pyq_service.get_unit_weightage()

@app.get("/plan")
def get_study_plan(hours: int = 20):
    return planner_service.generate_study_plan(total_study_hours=hours)

@app.get("/export-pdf")
def export_pdf(hours: int = 25):
    filename = report_service.generate_pdf_report(total_hours=hours)
    if os.path.exists(filename):
        return FileResponse(filename, media_type='application/pdf', filename="study_plan.pdf")
    raise HTTPException(status_code=404, detail="PDF generation failed.")