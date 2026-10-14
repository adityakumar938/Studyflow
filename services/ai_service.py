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

def _call_gemini_json(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing. Check your .env file.")
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
    return response.text


def extract_questions(pyq_text):
    """Send PYQ text to Gemini. Return a validated list of question dicts."""
    prompt = f"""Extract every exam question from this question paper.
Return ONLY JSON in this format:
{{"questions": [{{"question_text": "...", "year": 2023, "marks": 5}}]}}
Rules: year is the exam year as a number. marks is a number.
Copy the question text exactly. Do not invent questions.

QUESTION PAPER:
{pyq_text}
"""
    raw = _call_gemini_json(prompt)
    try:
        questions = json.loads(raw)["questions"]
        for q in questions:
            assert isinstance(q["question_text"], str) and q["question_text"].strip()
            assert isinstance(q["year"], int)
            assert isinstance(q["marks"], (int, float))
    except Exception as e:
        raise ValueError(f"Bad AI output: {e}")
    return questions

def map_questions_to_topics(questions, topics):
    """Return a dict: question index -> topic index (-1 means no match)."""
    topic_list = "\n".join(f"{i}: {t['name']}" for i, t in enumerate(topics))
    question_list = "\n".join(f"{i}: {q['question_text']}" for i, q in enumerate(questions))

    prompt = f"""Match each exam question to the syllabus topic it belongs to.
Return ONLY JSON in this format:
{{"mappings": [{{"question_index": 0, "topic_index": 0}}]}}
Rules: use only the numbers given below. Give one topic per question.
If no topic fits, use -1. Do not invent numbers.

TOPICS:
{topic_list}

QUESTIONS:
{question_list}
"""
    raw = _call_gemini_json(prompt)
    try:
        mappings = json.loads(raw)["mappings"]
        result = {}
        for m in mappings:
            qi, ti = m["question_index"], m["topic_index"]
            assert isinstance(qi, int) and 0 <= qi < len(questions)
            assert isinstance(ti, int) and -1 <= ti < len(topics)
            result[qi] = ti
    except Exception as e:
        raise ValueError(f"Bad AI output: {e}")

    for qi in range(len(questions)):
        result.setdefault(qi, -1)
    return result