from services.pdf_service import extract_text
from services.ai_service import extract_questions

text = extract_text("pyq.pdf")
questions = extract_questions(text)

for q in questions:
    print(q["year"], "|", q["marks"], "marks |", q["question_text"])
print("Total questions:", len(questions))