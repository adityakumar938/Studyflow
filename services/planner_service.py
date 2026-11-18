from services.pyq_service import PYQService

class PlannerService:
    def __init__(self, syllabus_path: str, pyq_path: str):
        self.pyq_service = PYQService(syllabus_path, pyq_path)

    def generate_study_plan(self, total_study_hours: int = 20) -> dict:
        weightages = self.pyq_service.get_unit_weightage()
        
        if not weightages:
            return {"message": "No weightage data available to generate plan."}
            
        total_questions = sum(weightages.values())
        
        plan = {}
        allocated_hours = 0
        
        sorted_units = sorted(weightages.items(), key=lambda x: x[1], reverse=True)
        
        for i, (unit, count) in enumerate(sorted_units):
            proportion = count / total_questions
            hours = round(proportion * total_study_hours, 1)
            
            if i == len(sorted_units) - 1:
                hours = round(total_study_hours - allocated_hours, 1)
                
            allocated_hours += hours
            plan[unit] = {
                "questions_appeared": count,
                "weightage_percentage": round(proportion * 100, 1),
                "recommended_hours": hours
            }
            
        return plan

