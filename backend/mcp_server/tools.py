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
    resource_map = {
        "medical": [
            {
                "name": "Emergency Hospital",
                "type": "hospital",
                "available": "Emergency and ambulance support"
            },
            {
                "name": "Nearest Ambulance Service",
                "type": "ambulance",
                "available": "Medical transport support"
            },
            {
                "name": "24/7 Pharmacy",
                "type": "pharmacy",
                "available": "Medicines and urgent supplies"
            }
        ],
        "fire": [
            {
                "name": "Nearest Fire Station",
                "type": "fire station",
                "available": "Fire rescue support"
            },
            {
                "name": "Emergency Hospital",
                "type": "hospital",
                "available": "Burn/injury treatment support"
            },
            {
                "name": "Safe Open Area",
                "type": "safe open area",
                "available": "Temporary safe gathering point"
            }
        ],
        "flood": [
            {
                "name": "Relief Shelter",
                "type": "relief shelter",
                "available": "Temporary shelter and basic supplies"
            },
            {
                "name": "Disaster Response Center",
                "type": "disaster response center",
                "available": "Flood support and rescue coordination"
            },
            {
                "name": "Emergency Hospital",
                "type": "hospital",
                "available": "Medical emergency support"
            }
        ],
        "earthquake": [
            {
                "name": "Safe Open Ground",
                "type": "safe open ground",
                "available": "Open area away from buildings"
            },
            {
                "name": "Emergency Hospital",
                "type": "hospital",
                "available": "Injury treatment support"
            },
            {
                "name": "Disaster Response Center",
                "type": "disaster response center",
                "available": "Rescue coordination"
            }
        ],
        "women": [
            {
                "name": "Nearest Police Station",
                "type": "police station",
                "available": "Immediate safety support"
            },
            {
                "name": "Women Help Desk",
                "type": "women help desk",
                "available": "Women safety assistance"
            },
            {
                "name": "Crowded Public Place",
                "type": "public place",
                "available": "Move here if you feel unsafe"
            }
        ],
        "scam": [
            {
                "name": "Cyber Crime Help",
                "type": "cyber crime police station",
                "available": "Report online fraud or scam"
            },
            {
                "name": "Nearest Police Station",
                "type": "police station",
                "available": "File complaint if needed"
            }
        ],
        "general": [
            {
                "name": "Nearest Police Station",
                "type": "police station",
                "available": "24/7 support"
            },
            {
                "name": "Emergency Hospital",
                "type": "hospital",
                "available": "Emergency medical support"
            }
        ]
    }

    selected_resources = resource_map.get(
        emergency_type.lower(),
        resource_map["general"]
    )

    return {
        "tool": "Nearby Resource Finder Tool",
        "note": "Demo resource finder using Google Maps search links.",
        "location": location,
        "emergency_type": emergency_type,
        "resources": selected_resources
    }