from utils.groq_helper import analyze_with_groq
from mcp_server.server import call_mcp_tool

def generate_action_plan(situation):
    groq_result = generate_plan_with_groq(situation)

    if groq_result and "error" not in groq_result:
     groq_result["agent"] = "Action Planning Agent"
     groq_result["analysis_source"] = "Groq LLM + Planning Agent"

    crisis_type = groq_result.get("crisis_type", "general")

    mcp_plan = call_mcp_tool(
        "generate_disaster_plan",
        disaster_type=crisis_type
    )

    groq_result["mcp_plan"] = mcp_plan
    groq_result["mcp_tool_used"] = "generate_disaster_plan"

    return groq_result

    return rule_based_action_plan(situation)


def generate_plan_with_groq(situation):
    prompt = f"""
You are the Action Planning Agent inside SafeSphere AI.

Create a practical emergency action plan.

Situation:
{situation}

Return ONLY valid JSON with this exact structure:
{{
  "crisis_type": "flood | fire | earthquake | storm | accident | medical | general",
  "immediate_plan": ["step 1", "step 2", "step 3"],
  "next_30_minutes": ["step 1", "step 2", "step 3"],
  "emergency_kit": ["item 1", "item 2", "item 3"],
  "avoid": ["thing to avoid 1", "thing to avoid 2"],
  "safe_message": "short message user can send to family",
  "emergency_contacts": [
    "112 - National Emergency Helpline",
    "101 - Fire",
    "108 - Ambulance"
  ]
}}

Rules:
- Give situation-specific steps.
- If fire, prioritize evacuation and avoiding smoke.
- If flood, prioritize higher ground and avoiding floodwater.
- If medical emergency, recommend ambulance/emergency services where appropriate.
- Do not give risky instructions.
- Keep it practical and India-relevant.
"""
    return analyze_with_groq(prompt)


def rule_based_action_plan(situation):
    situation = situation.lower()

    if "flood" in situation:
        crisis_type = "Flood"
        plan = [
            "Move to higher ground immediately",
            "Carry essential medicines",
            "Keep important documents safe",
            "Avoid walking through floodwater",
            "Monitor local emergency alerts"
        ]
    elif "fire" in situation:
        crisis_type = "Fire"
        plan = [
            "Evacuate immediately",
            "Use stairs instead of elevators",
            "Stay low to avoid smoke",
            "Call emergency services",
            "Move to a designated safe area"
        ]
    elif "earthquake" in situation:
        crisis_type = "Earthquake"
        plan = [
            "Drop, Cover and Hold",
            "Stay away from windows",
            "Move to open space after shaking stops",
            "Check for injuries",
            "Follow official instructions"
        ]
    else:
        crisis_type = "General"
        plan = [
            "Stay calm",
            "Assess the situation",
            "Contact trusted people",
            "Follow local authority guidance"
        ]

    return {
        "agent": "Action Planning Agent",
        "analysis_source": "Rule-based fallback",
        "crisis_type": crisis_type,
        "immediate_plan": plan,
"mcp_plan": call_mcp_tool(
    "generate_disaster_plan",
    disaster_type=crisis_type
),
"mcp_tool_used": "generate_disaster_plan",
        "next_30_minutes": [
            "Keep monitoring the situation",
            "Contact trusted people",
            "Follow official instructions"
        ],
        "emergency_kit": [
            "Phone",
            "Charger",
            "Medicines",
            "Water",
            "Important documents"
        ],
        "avoid": [
            "Do not panic",
            "Do not ignore official warnings"
        ],
        "safe_message": "I am safe for now and following emergency guidance.",
        "emergency_contacts": [
            "112 - National Emergency Helpline",
            "101 - Fire",
            "108 - Ambulance"
        ]
    }