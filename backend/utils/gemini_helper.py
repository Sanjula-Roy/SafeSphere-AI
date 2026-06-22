import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def analyze_with_gemini(prompt):
    if not GOOGLE_API_KEY:
        return None

    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)

        response = client.models.generate_content(
            model="models/gemini-2.0-flash-lite",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {
            "error": "Gemini analysis failed",
            "details": str(e)
        }