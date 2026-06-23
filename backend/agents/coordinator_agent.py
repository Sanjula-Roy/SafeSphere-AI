from agents.threat_agent import analyze_threat
from agents.privacy_agent import mask_sensitive_data
from agents.safety_agent import assess_personal_safety
from agents.crisis_agent import assess_crisis
from agents.planning_agent import generate_action_plan
from agents.explanation_agent import generate_explanation
from agents.emotional_support_agent import detect_emotional_distress, emotional_support_response


def coordinate_safety_request(user_input):
    text = user_input.lower()

    results = {
        "agent": "Safety Coordinator Agent",
        "input": user_input,
        "selected_agents": [],
        "final_response": {}
    }
    SAFETY_CONTEXT_KEYWORDS = [
    "sos", "emergency", "help me", "flood", "fire", "earthquake",
    "storm", "disaster", "medical", "ambulance", "accident",
    "unsafe", "following", "harassing", "stalking", "cab",
    "driver", "knife", "weapon", "scam", "fraud", "otp",
    "bank", "kyc", "privacy", "aadhaar", "pan", "private", "kill", "harm", "touch", "abuse"
]

    is_safety_context = any(word in text for word in SAFETY_CONTEXT_KEYWORDS)

    emotional_check = None

    if not is_safety_context:
     emotional_check = detect_emotional_distress(user_input)

    if emotional_check and emotional_check.get("is_emotional_distress") is True:
        results["selected_agents"].append("Emotional Support Agent")
        results["final_response"]["emotional_detection"] = emotional_check
        results["final_response"]["emotional_support"] = emotional_support_response(user_input)

    if any(word in text for word in ["otp", "bank", "click", "kyc", "password", "upi", "blocked", "verify"]):
        results["selected_agents"].append("Threat Detection Agent")
        results["final_response"]["threat_analysis"] = analyze_threat(user_input)

    if any(word in text for word in ["aadhaar", "pan", "phone", "email", "@"]):
        results["selected_agents"].append("Privacy & Security Agent")
        results["final_response"]["privacy_scan"] = mask_sensitive_data(user_input)

    if any(word in text for word in ["unsafe", "following", "alone", "stalking", "harassment", "dark road"]):
        results["selected_agents"].append("Personal Safety Agent")
        results["final_response"]["personal_safety"] = assess_personal_safety(user_input)

    if any(word in text for word in ["flood", "fire", "earthquake", "storm", "heavy rain", "accident", "medical"]):
        results["selected_agents"].append("Crisis Assessment Agent")
        results["selected_agents"].append("Action Planning Agent")
        results["final_response"]["crisis_assessment"] = assess_crisis(user_input)
        results["final_response"]["action_plan"] = generate_action_plan(user_input)

    if not results["selected_agents"]:
        results["selected_agents"].append("General Safety Guidance")
        results["final_response"]["message"] = (
            "SafeSphere could not detect a specific crisis type, but recommends staying alert, "
            "avoiding risky actions, and contacting trusted people or emergency services if needed."
        )

    results["summary"] = generate_summary(results)
    results["explanation"] = generate_explanation(results)

    return results


def generate_summary(results):
    agents = ", ".join(results["selected_agents"])
    return f"SafeSphere analyzed the request using: {agents}."