from services.pdf_service import extract_text
from services.ai_service import extract_topics

text = extract_text("syllabus.pdf")
topics = extract_topics(text)

for t in topics:
    print(t["unit"], "|", t["name"], "|", t["difficulty"])
print("Total topics:", len(topics))