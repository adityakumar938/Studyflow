import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key:
    raise SystemExit("GEMINI_API_KEY missing. Check your .env file.")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents="Reply with one short sentence confirming you are working.",
    )
    print(response.text)
except Exception as e:
    print(f"Gemini call failed: {type(e).__name__}: {e}")