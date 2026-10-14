import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def extract_topics(syllabus_text):
    """Send syllabus text to Gemini. Return a validated list of topic dicts."""
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing. Check your .env file.")

    prompt = f"""Extract the study topics from this syllabus.
Return ONLY JSON in this format:
{{"topics": [{{"name": "...", "unit": "...", "estimated_hours": 2, "difficulty": "easy"}}]}}
Rules: difficulty must be easy, medium or hard. Do not invent topics.

SYLLABUS:
{syllabus_text}
"""

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
        raise RuntimeError(f"Gemini call failed: {type(e).__name__}: {e}")

    return _validate_topics(response.text)


def _validate_topics(raw_text):
    try:
        topics = json.loads(raw_text)["topics"]
        for t in topics:
            assert isinstance(t["name"], str) and t["name"].strip()
            assert t["difficulty"] in ("easy", "medium", "hard")
            assert isinstance(t["estimated_hours"], (int, float))
    except Exception as e:
        raise ValueError(f"Bad AI output: {e}")
    return topics