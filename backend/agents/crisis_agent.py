from utils.groq_helper import analyze_with_groq


def assess_crisis(situation):
    groq_result = analyze_crisis_with_groq(situation)

    if groq_result and "error" not in groq_result:
        groq_result["agent"] = "Crisis Assessment Agent"
        groq_result["analysis_source"] = "Groq LLM + Crisis Agent"
        return normalize_crisis_score(groq_result)

    return rule_based_crisis(situation)


def analyze_crisis_with_groq(situation):
    prompt = f"""
You are the Crisis Assessment Agent inside SafeSphere AI.

Analyze the emergency or disaster situation.

Situation:
{situation}

Return ONLY valid JSON with this exact structure:
{{
  "risk_level": "Low | Medium | High",
  "risk_score": number between 0 and 100,
  "crisis_type": "flood | fire | earthquake | storm | accident | medical | general",
  "situation_summary": "brief summary",
  "why_this_is_risky": "explain the risk",
  "danger_signs": ["sign 1", "sign 2", "sign 3"],
  "recommended_priority": "monitor | prepare | evacuate | call emergency services",
  "emergency_contacts": [
    "112 - National Emergency Helpline",
    "101 - Fire",
    "108 - Ambulance"
  ]
}}

Rules:
- If there is fire, flood, earthquake, severe injury, unconscious person, explosion, or immediate danger, risk should usually be High.
- If risk_level is High, risk_score must be 70 to 100.
- If risk_level is Medium, risk_score must be 40 to 69.
- If risk_level is Low, risk_score must be 0 to 39.
- Give India-relevant emergency contacts.
"""
    return analyze_with_groq(prompt)


def normalize_crisis_score(result):
    risk_level = result.get("risk_level", "Low")

    if risk_level == "High" and result.get("risk_score", 0) < 70:
        result["risk_score"] = 90
    elif risk_level == "Medium" and result.get("risk_score", 0) < 40:
        result["risk_score"] = 55
    elif risk_level == "Low" and result.get("risk_score", 100) > 39:
        result["risk_score"] = 25

    return result


def rule_based_crisis(situation):
    situation = situation.lower()
    risk_score = 0
    reasons = []

    high_risk = ["flood", "earthquake", "fire", "building collapse", "heart attack", "explosion", "tsunami"]
    medium_risk = ["storm", "heavy rain", "injury", "accident", "fever", "power outage"]

    for word in high_risk:
        if word in situation:
            risk_score += 30
            reasons.append(f"Detected high-risk event: {word}")

    for word in medium_risk:
        if word in situation:
            risk_score += 15
            reasons.append(f"Detected medium-risk event: {word}")

    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "Crisis Assessment Agent",
        "analysis_source": "Rule-based fallback",
        "risk_level": risk_level,
        "risk_score": min(risk_score, 100),
        "crisis_type": "general",
        "situation_summary": "Crisis situation detected.",
        "why_this_is_risky": "The system found emergency-related indicators.",
        "danger_signs": reasons,
        "recommended_priority": "prepare",
        "emergency_contacts": [
            "112 - National Emergency Helpline",
            "101 - Fire",
            "108 - Ambulance"
        ]
    }