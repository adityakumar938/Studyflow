from services.planner_service import PlannerService

# Initialize planner with your PDF files
planner = PlannerService("syllabus.pdf", "pyq.pdf")

# Generate a plan for 25 total study hours
print("--- Smart Study Plan (25 Hours) ---")
plan = planner.generate_study_plan(total_study_hours=25)

for unit, details in plan.items():
    print(f"\n{unit}:")
    print(f"  - PYQ Questions: {details['questions_appeared']}")
    print(f"  - Weightage: {details['weightage_percentage']}%")
    print(f"  - Recommended Study Time: {details['recommended_hours']} hours")