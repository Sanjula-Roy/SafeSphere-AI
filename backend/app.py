from flask import Flask, jsonify, request
from flask_cors import CORS

from agents.threat_agent import analyze_threat
from agents.privacy_agent import mask_sensitive_data
from agents.safety_agent import assess_personal_safety
from agents.crisis_agent import assess_crisis
from agents.planning_agent import generate_action_plan
from agents.coordinator_agent import coordinate_safety_request
from agents.emotional_support_agent import emotional_support_chat
from mcp_server.server import call_mcp_tool

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "project": "SafeSphere AI",
        "status": "running",
        "message": "Welcome to SafeSphere AI"
    })


@app.route("/analyze-threat", methods=["POST"])
def analyze_threat_route():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    return jsonify(analyze_threat(message))


@app.route("/mask-sensitive-data", methods=["POST"])
def mask_sensitive_data_route():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    return jsonify(mask_sensitive_data(text))


@app.route("/personal-safety", methods=["POST"])
def personal_safety_route():
    data = request.get_json()
    situation = data.get("situation", "")

    if not situation:
        return jsonify({"error": "Situation is required"}), 400

    return jsonify(assess_personal_safety(situation))


@app.route("/assess-crisis", methods=["POST"])
def crisis_route():

    data = request.get_json()
    situation = data.get("situation", "")

    if not situation:
        return jsonify({
            "error": "Situation is required"
        }), 400

    return jsonify(assess_crisis(situation))

@app.route("/action-plan", methods=["POST"])
def action_plan_route():

    data = request.get_json()
    situation = data.get("situation", "")

    if not situation:
        return jsonify({
            "error": "Situation is required"
        }), 400

    return jsonify(generate_action_plan(situation))

@app.route("/safe-sphere", methods=["POST"])
def safe_sphere_route():
    data = request.get_json()
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({"error": "Input is required"}), 400

    return jsonify(coordinate_safety_request(user_input))

@app.route("/emotional-chat", methods=["POST"])
def emotional_chat_route():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    return jsonify(emotional_support_chat(message))

@app.route("/mcp-test", methods=["POST"])
def mcp_test_route():
    data = request.get_json()

    tool_name = data.get("tool_name", "")
    args = data.get("args", {})

    result = call_mcp_tool(tool_name, **args)

    return jsonify({
        "mcp_server": "SafeSphere MCP Server",
        "tool_called": tool_name,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)