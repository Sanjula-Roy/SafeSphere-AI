from utils.groq_helper import analyze_with_groq
from mcp_server.server import call_mcp_tool


def analyze_threat(message):
    groq_result = analyze_threat_with_groq(message)

    mcp_result = call_mcp_tool(
        "verify_scam_warning",
        message=message
    )

    nearby_resources = call_mcp_tool(
        "find_nearby_resources",
        location="demo area",
        emergency_type="scam"
    )

    if groq_result and "error" not in groq_result:
        groq_result["agent"] = "Threat Detection Agent"
        groq_result["analysis_source"] = "Groq LLM + Threat Agent"

        groq_result["mcp_verification"] = mcp_result
        groq_result["mcp_tool_used"] = "verify_scam_warning"

        groq_result["nearby_resources"] = nearby_resources
        groq_result["resource_tool_used"] = "find_nearby_resources"

        return normalize_threat_score(groq_result)

    return rule_based_threat_analysis(message, mcp_result, nearby_resources)


def analyze_threat_with_groq(message):
    prompt = f"""
You are the Threat Detection Agent inside SafeSphere AI.

Analyze this message for scam, fraud, phishing, UPI fraud, fake bank message, OTP fraud, malicious links, or social engineering.

Message:
{message}

Return ONLY valid JSON with this exact structure:
{{
  "risk_level": "Low | Medium | High",
  "risk_score": number between 0 and 100,
  "threat_type": "phishing | fraud | scam | suspicious | safe",
  "situation_summary": "brief summary",
  "why_this_is_risky": "explanation",
  "warning_signs": ["sign 1", "sign 2", "sign 3"],
  "recommended_actions": ["action 1", "action 2", "action 3"],
  "safe_reply": "short safe reply or action suggestion",
  "security_tips": ["tip 1", "tip 2", "tip 3"]
}}

Rules:
- If OTP, password, KYC, bank blocked, urgent click, suspicious link, or payment request exists, risk should usually be High.
- If risk_level is High, risk_score must be 70 to 100.
- If Medium, risk_score must be 40 to 69.
- If Low, risk_score must be 0 to 39.
- Do not ask the user to click suspicious links.
"""
    return analyze_with_groq(prompt)


def normalize_threat_score(result):
    risk_level = result.get("risk_level", "Low")

    if risk_level == "High" and result.get("risk_score", 0) < 70:
        result["risk_score"] = 90
    elif risk_level == "Medium" and result.get("risk_score", 0) < 40:
        result["risk_score"] = 55
    elif risk_level == "Low" and result.get("risk_score", 100) > 39:
        result["risk_score"] = 25

    return result


def rule_based_threat_analysis(message, mcp_result=None, nearby_resources=None):
    import re

    message_lower = message.lower()
    risk_score = 0
    reasons = []

    risky_keywords = [
        "urgent", "blocked", "verify", "password", "otp",
        "click", "account suspended", "bank", "upi",
        "kyc", "lottery", "winner", "prize", "limited time"
    ]

    for word in risky_keywords:
        if word in message_lower:
            risk_score += 10
            reasons.append(f"Contains suspicious word: {word}")

    if re.search(r"(https?://\S+|www\.\S+)", message):
        risk_score += 25
        reasons.append("Contains a URL/link")

    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if mcp_result is None:
        mcp_result = call_mcp_tool(
            "verify_scam_warning",
            message=message
        )

    if nearby_resources is None:
        nearby_resources = call_mcp_tool(
            "find_nearby_resources",
            location="demo area",
            emergency_type="scam"
        )

    return {
        "agent": "Threat Detection Agent",
        "analysis_source": "Rule-based fallback",
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "threat_type": "suspicious",
        "situation_summary": "Potential scam or fraud message detected.",
        "why_this_is_risky": "The message contains scam-like indicators.",
        "warning_signs": reasons,
        "recommended_actions": [
            "Do not click suspicious links",
            "Do not share OTP, password, or banking details",
            "Contact the organization through official channels"
        ],
        "safe_reply": "I will verify this through official support channels.",
        "security_tips": [
            "Never share OTPs",
            "Check sender identity",
            "Avoid urgent payment or login links"
        ],
        "mcp_verification": mcp_result,
        "mcp_tool_used": "verify_scam_warning",
        "nearby_resources": nearby_resources,
        "resource_tool_used": "find_nearby_resources"
    }