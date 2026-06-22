import json
from utils.groq_helper import analyze_with_groq


def generate_explanation(coordinator_result):
    groq_result = generate_explanation_with_groq(coordinator_result)

    if groq_result and "error" not in groq_result:
        groq_result["agent"] = "Explanation Agent"
        groq_result["analysis_source"] = "Groq LLM + Explanation Agent"
        return groq_result

    return fallback_explanation(coordinator_result)


def generate_explanation_with_groq(coordinator_result):
    prompt = f"""
You are the Explanation Agent inside SafeSphere AI.

Create a clear, helpful, AI-generated final response based on all agent outputs.

Agent result:
{json.dumps(coordinator_result, indent=2)}

Return ONLY valid JSON with this exact structure:
{{
  "overall_risk": "Low | Medium | High",
  "final_advice": "personalized final advice",
  "short_summary": "short summary of the situation",
  "what_to_do_now": ["step 1", "step 2", "step 3"],
  "why_agents_were_selected": ["reason 1", "reason 2"],
  "important_note": "important safety note"
}}

Rules:
- Do not give generic advice.
- Use the actual situation and agent outputs.
- If any agent reports High risk, overall risk should usually be High.
- Keep advice practical, calm, and safe.
- For danger, recommend emergency services.
- For scams, recommend not paying, not clicking, and verifying through official channels.
- For privacy, recommend masking sensitive details.
"""
    return analyze_with_groq(prompt)


def fallback_explanation(coordinator_result):
    selected_agents = coordinator_result.get("selected_agents", [])

    return {
        "agent": "Explanation Agent",
        "analysis_source": "Rule-based fallback",
        "overall_risk": "Medium",
        "final_advice": "SafeSphere detected a possible safety concern. Please stay cautious and follow the recommended agent actions.",
        "short_summary": "SafeSphere analyzed your situation using specialized safety agents.",
        "what_to_do_now": [
            "Review the risk assessment",
            "Follow the recommended actions",
            "Contact emergency services if you are in immediate danger"
        ],
        "why_agents_were_selected": [
            f"{agent} was selected based on the situation details."
            for agent in selected_agents
        ],
        "important_note": "This assistant supports safety planning but does not replace emergency services."
    }