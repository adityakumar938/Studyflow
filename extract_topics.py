import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise SystemExit("GEMINI_API_KEY missing. Check your .env file.")

# 1. Read the PDF
reader = PdfReader("syllabus.pdf")
text = "\n".join(page.extract_text() for page in reader.pages)

# 2. Prompt: ask for JSON only
prompt = f"""Extract the study topics from this syllabus.
Return ONLY JSON in this format:
{{"topics": [{{"name": "...", "unit": "...", "estimated_hours": 2, "difficulty": "easy"}}]}}
Rules: difficulty must be easy, medium or hard. Do not invent topics.

SYLLABUS:
{text}
"""

# 3. Ask Gemini
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=60000),
)
try:
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
except Exception as e:
    raise SystemExit(f"Gemini call failed: {type(e).__name__}: {e}")

# 4. Validate the answer
try:
    data = json.loads(response.text)
    topics = data["topics"]
    for t in topics:
        assert isinstance(t["name"], str) and t["name"].strip()
        assert t["difficulty"] in ("easy", "medium", "hard")
        assert isinstance(t["estimated_hours"], (int, float))
except Exception as e:
    raise SystemExit(f"Bad AI output: {e}\n{response.text}")

# 5. Show result
for t in topics:
    print(t["unit"], "|", t["name"], "|", t["difficulty"], "|", t["estimated_hours"], "h")
print("Total topics:", len(topics))