def get_emergency_contacts(category="general"):
    contacts = {
        "general": [
            {"name": "National Emergency Helpline", "number": "112"},
            {"name": "Police", "number": "100"},
            {"name": "Ambulance", "number": "108"},
            {"name": "Fire", "number": "101"}
        ],
        "women": [
            {"name": "National Emergency Helpline", "number": "112"},
            {"name": "Women Helpline", "number": "1091"},
            {"name": "Women Helpline", "number": "181"},
            {"name": "Police", "number": "100"}
        ],
        "medical": [
            {"name": "Ambulance", "number": "108"},
            {"name": "National Emergency Helpline", "number": "112"}
        ],
        "fire": [
            {"name": "Fire", "number": "101"},
            {"name": "National Emergency Helpline", "number": "112"}
        ],
        "disaster": [
            {"name": "National Emergency Helpline", "number": "112"},
            {"name": "Disaster Management Helpline", "number": "1078"}
        ]
    }

    return {
        "tool": "Emergency Contacts Tool",
        "category": category,
        "contacts": contacts.get(category, contacts["general"])
    }


def generate_sos_message(situation, contact_type="family"):
    return {
        "tool": "SOS Generator Tool",
        "contact_type": contact_type,
        "message": (
            f"I need help. Situation: {situation}. "
            "Please call me immediately and track my location if available."
        )
    }


def verify_scam_warning(message):
    risky_terms = ["otp", "kyc", "password", "bank", "click", "verify", "upi", "blocked"]

    found = [
        term for term in risky_terms
        if term in message.lower()
    ]

    return {
        "tool": "Scam Verification Tool",
        "is_suspicious": len(found) > 0,
        "matched_warning_signs": found,
        "tool_advice": "Do not click suspicious links or share OTP/passwords."
    }


def generate_disaster_plan(disaster_type):
    plans = {
        "flood": [
            "Move to higher ground",
            "Avoid floodwater",
            "Keep medicines and documents safe",
            "Follow official alerts"
        ],
        "fire": [
            "Evacuate immediately",
            "Avoid smoke",
            "Use stairs instead of elevators",
            "Call fire services"
        ],
        "earthquake": [
            "Drop, Cover, and Hold",
            "Stay away from windows",
            "Move to open space after shaking stops"
        ],
        "medical": [
            "Call ambulance if symptoms are serious",
            "Keep the person calm",
            "Do not give food or water if unconscious",
            "Share location with emergency responders"
        ]
    }

    return {
        "tool": "Disaster Planning Tool",
        "disaster_type": disaster_type,
        "plan": plans.get(disaster_type.lower(), [
            "Stay calm",
            "Move to a safe location",
            "Contact emergency services",
            "Follow official instructions"
        ])
    }


def find_nearby_resources(location="demo area", emergency_type="general"):
    return {
        "tool": "Nearby Resource Finder Tool",
        "note": "Demo resource finder using sample data.",
        "location": location,
        "emergency_type": emergency_type,
        "resources": [
            {
                "name": "Nearest Government Hospital",
                "type": "hospital",
                "distance": "2.1 km",
                "available": "Emergency care available"
            },
            {
                "name": "Nearest Police Station",
                "type": "police",
                "distance": "1.4 km",
                "available": "24/7 support"
            },
            {
                "name": "Community Relief Center",
                "type": "shelter",
                "distance": "3.0 km",
                "available": "Temporary shelter support"
            }
        ]
    }