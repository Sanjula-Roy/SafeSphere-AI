from utils.groq_helper import analyze_with_groq
from mcp_server.server import call_mcp_tool


def assess_personal_safety(situation):
    print("\n=== PERSONAL SAFETY INPUT ===")
    print(situation)

    groq_result = analyze_personal_safety_with_groq(situation)

    print("\n=== GROQ RESULT ===")
    print(groq_result)

    if groq_result and "error" not in groq_result:
        groq_result["agent"] = "Personal Safety Agent"
        groq_result["analysis_source"] = "Groq LLM + Safety Agent"

        groq_result["emergency_contacts"] = call_mcp_tool(
            "get_emergency_contacts",
            category="women"
        )
        groq_result["mcp_tool_used"] = "get_emergency_contacts"

        groq_result["nearby_resources"] = call_mcp_tool(
            "find_nearby_resources",
            location="demo area",
            emergency_type="women"
        )
        groq_result["resource_tool_used"] = "find_nearby_resources"

        risk_level = groq_result.get("risk_level", "Low")

        if risk_level == "High" and groq_result.get("risk_score", 0) < 70:
            groq_result["risk_score"] = 90
        elif risk_level == "Medium" and groq_result.get("risk_score", 0) < 40:
            groq_result["risk_score"] = 55
        elif risk_level == "Low" and groq_result.get("risk_score", 100) > 39:
            groq_result["risk_score"] = 25

        return groq_result

    return rule_based_personal_safety(situation)


def analyze_personal_safety_with_groq(situation):
    prompt = f"""
You are an expert Personal Safety Response Agent inside SafeSphere AI.

Analyze the situation and create a personalized safety response.

User Situation:
{situation}

Return ONLY valid JSON with this exact structure:
{{
  "risk_level": "Low | Medium | High",
  "risk_score": number between 0 and 100,
  "situation_summary": "brief summary of what is happening",
  "why_this_is_risky": "explain why this situation may or may not be risky",
  "next_5_minutes": [
    "specific action 1",
    "specific action 2",
    "specific action 3"
  ],
  "next_30_minutes": [
    "specific action 1",
    "specific action 2",
    "specific action 3"
  ],
  "custom_sos_message": "ready-to-send emergency/check-in message",
  "emergency_contacts": [
    "112 - National Emergency Helpline",
    "100 - Police",
    "1091 - Women Helpline",
    "181 - Women Helpline"
  ],
  "safety_tips": [
    "specific safety tip 1",
    "specific safety tip 2",
    "specific safety tip 3"
  ],
  "safety_disclaimer": "This assistant supports safety planning but does not replace emergency services."
}}

Rules:
- Understand the whole situation, not just keywords.
- If the user says alone=no, do NOT treat being alone as danger.
- If the user says following=no or harassing=no, do NOT treat those words as danger.
- If location is cab but there is no threat, risk should usually be Low or Medium, not High.
- If weapon, knife, attack, stabbing, threat, stalking, harassment, or immediate physical danger exists, risk should usually be High.
- If risk_level is High, risk_score must be between 70 and 100.
- If risk_level is Medium, risk_score must be between 40 and 69.
- If risk_level is Low, risk_score must be between 0 and 39.
- Give practical, calm, situation-specific actions.
- Do not suggest confronting dangerous people.
- SOS message must be short, urgent, and ready to copy/send.
- Emergency contacts should be relevant to India.
"""
    return analyze_with_groq(prompt)


def rule_based_personal_safety(situation):
    situation = situation.lower()

    risk_score = 0
    reasons = []

    if "alone=yes" in situation:
        risk_score += 20
        reasons.append("User reported being alone")

    if "following=yes" in situation:
        risk_score += 40
        reasons.append("User reported being followed")

    if "harassing=yes" in situation:
        risk_score += 40
        reasons.append("User reported harassment")

    if "stalking" in situation:
        risk_score += 50
        reasons.append("Stalking indicator detected")

    if "dark road" in situation:
        risk_score += 30
        reasons.append("Dark or isolated area detected")

    if "knife" in situation or "weapon" in situation:
        risk_score += 80
        reasons.append("Weapon-related danger detected")

    if "stabbing" in situation or "stab" in situation:
        risk_score += 80
        reasons.append("Stabbing-related threat detected")

    if "attacked" in situation or "threat" in situation:
        risk_score += 60
        reasons.append("Immediate threat indicator detected")

    if "alone=yes" in situation and ("following=yes" in situation or "harassing=yes" in situation):
        risk_score += 20
        reasons.append("High-risk combination detected")

    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "agent": "Personal Safety Agent",
        "analysis_source": "Rule-based fallback",
        "risk_level": risk_level,
        "risk_score": min(risk_score, 100),
        "situation_summary": "Personal safety situation detected.",
        "why_this_is_risky": "The system found safety-related indicators in the user's report.",
        "next_5_minutes": get_actions(risk_level),
        "next_30_minutes": get_follow_up_actions(risk_level),
        "custom_sos_message": generate_sos_message(risk_level),
        "emergency_contacts": call_mcp_tool(
            "get_emergency_contacts",
            category="women"
        ),
        "mcp_tool_used": "get_emergency_contacts",
        "nearby_resources": call_mcp_tool(
            "find_nearby_resources",
            location="demo area",
            emergency_type="women"
        ),
        "resource_tool_used": "find_nearby_resources",
        "safety_tips": get_safety_tips(risk_level),
        "safety_disclaimer": "This assistant supports safety planning but does not replace emergency services.",
        "reasons": reasons
    }


def get_actions(risk_level):
    if risk_level == "High":
        return [
            "Move to a crowded or public place immediately",
            "Call emergency services if you feel in immediate danger",
            "Share your live location with trusted contacts",
            "Call a trusted person and stay on the phone",
            "Avoid confronting the person directly"
        ]

    if risk_level == "Medium":
        return [
            "Stay alert and keep your phone accessible",
            "Call a trusted friend or family member",
            "Move toward a public or well-lit area"
        ]

    return [
        "Stay aware of your surroundings",
        "Keep emergency contacts accessible",
        "Share your location with a trusted contact if unsure"
    ]


def get_follow_up_actions(risk_level):
    if risk_level == "High":
        return [
            "Report the incident to police or local authorities",
            "Inform family or trusted contacts about what happened",
            "Save screenshots, cab details, location, or any evidence if it is safe to do so"
        ]

    if risk_level == "Medium":
        return [
            "Continue sharing location until you feel safe",
            "Avoid isolated areas",
            "Document details if the situation becomes worse"
        ]

    return [
        "Continue monitoring the situation",
        "Avoid sharing unnecessary personal details",
        "Keep emergency contacts ready"
    ]


def get_safety_tips(risk_level):
    if risk_level == "High":
        return [
            "Prioritize escape and visibility over confrontation",
            "Stay on a call with someone you trust",
            "If in a vehicle, try to exit only at a safe public place"
        ]

    if risk_level == "Medium":
        return [
            "Trust your instincts if something feels wrong",
            "Keep your phone charged and accessible",
            "Share trip/location details with someone trusted"
        ]

    return [
        "Stay aware of your surroundings",
        "Keep trusted contacts informed when traveling",
        "Use verified transport and avoid sharing private information"
    ]


def generate_sos_message(risk_level):
    if risk_level == "High":
        return (
            "I feel unsafe and may need urgent assistance. "
            "Please call me immediately and track my location. "
            "If I do not respond, contact emergency services."
        )

    if risk_level == "Medium":
        return (
            "I feel uncomfortable and want someone to stay connected with me. "
            "Please keep your phone available."
        )

    return "I am checking in. Please keep your phone available."