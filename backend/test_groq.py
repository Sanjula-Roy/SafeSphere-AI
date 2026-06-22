from utils.groq_helper import analyze_with_groq

prompt = """
Return ONLY valid JSON:
{
  "message": "Groq is connected",
  "status": "success"
}
"""

result = analyze_with_groq(prompt)
print(result)