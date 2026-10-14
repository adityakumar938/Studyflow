from services.pdf_service import extract_text
from services.ai_service import extract_topics, extract_questions, map_questions_to_topics

topics = extract_topics(extract_text("syllabus.pdf"))
questions = extract_questions(extract_text("pyq.pdf"))
mapping = map_questions_to_topics(questions, topics)

for qi, q in enumerate(questions):
    ti = mapping[qi]
    name = topics[ti]["name"] if ti >= 0 else "UNMAPPED"
    print(q["year"], "|", q["question_text"][:45], "->", name)