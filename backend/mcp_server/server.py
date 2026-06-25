from mcp_server.tools import (
    get_emergency_contacts,
    generate_sos_message,
    verify_scam_warning,
    generate_disaster_plan,
    find_nearby_resources
)


def call_mcp_tool(tool_name, **kwargs):
    if tool_name == "get_emergency_contacts":
        return get_emergency_contacts(kwargs.get("category", "general"))

    if tool_name == "generate_sos_message":
        return generate_sos_message(
            kwargs.get("situation", ""),
            kwargs.get("contact_type", "family")
        )

    if tool_name == "verify_scam_warning":
        return verify_scam_warning(kwargs.get("message", ""))

    if tool_name == "generate_disaster_plan":
        return generate_disaster_plan(kwargs.get("disaster_type", "general"))

    if tool_name == "find_nearby_resources":
        return find_nearby_resources(
            kwargs.get("location", "demo area"),
            kwargs.get("emergency_type", "general")
        )

    return {
        "error": "Unknown MCP tool",
        "available_tools": [
            "get_emergency_contacts",
            "generate_sos_message",
            "verify_scam_warning",
            "generate_disaster_plan",
            "find_nearby_resources"
        ]
    }