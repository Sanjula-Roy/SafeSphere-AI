from utils.gemini_helper import analyze_with_gemini

prompt = """
Return ONLY valid JSON:
{
  "message": "Gemini is connected",
  "status": "success"
}
"""

result = analyze_with_gemini(prompt)

print(result)