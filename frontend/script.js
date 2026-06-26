let selectedHelpType = "";

function selectHelp(type) {
    selectedHelpType = type;
    const box = document.getElementById("questionsBox");
    const input = document.getElementById("userInput");

    let html = "";
    let prompt = "";

    if (type === "scam") {
        html = `
            <h3>🚨 Scam / Fraud Help</h3>
            <label>What happened?</label>
            <input id="q1" placeholder="Example: I received a bank message with a link">
            <label>Did it ask for OTP/password/KYC?</label>
            <select id="q2">
                <option>Yes</option>
                <option>No</option>
                <option>Not sure</option>
            </select>
            <button onclick="buildPrompt('scam')">Generate Guided Prompt</button>
        `;
        prompt = "I may have received a scam or fraud message.";
    }

    if (type === "women") {
        html = `
            <h3>👩 Women Safety Mode</h3>
            <label>Are you alone?</label>
            <select id="q1">
                <option>Yes</option>
                <option>No</option>
            </select>
            <label>Is someone following or harassing you?</label>
            <select id="q2">
                <option>Yes</option>
                <option>No</option>
                <option>Not sure</option>
            </select>
            <label>Where are you?</label>
            <input id="q3" placeholder="Example: near station, cab, dark road">
            <button onclick="buildPrompt('women')">Generate Guided Prompt</button>
        `;
        prompt = "I feel unsafe and need personal safety help.";
    }

    if (type === "medical") {
        html = `
            <h3>🏥 Medical Emergency</h3>
            <label>What is the medical issue?</label>
            <input id="q1" placeholder="Example: chest pain, injury, fever">
            <label>Is the person conscious?</label>
            <select id="q2">
                <option>Yes</option>
                <option>No</option>
                <option>Not sure</option>
            </select>
            <button onclick="buildPrompt('medical')">Generate Guided Prompt</button>
        `;
        prompt = "There is a medical emergency.";
    }

    if (type === "disaster") {
        html = `
            <h3>🌊 Disaster Response</h3>
            <label>Type of disaster</label>
            <select id="q1">
                <option>Flood</option>
                <option>Fire</option>
                <option>Earthquake</option>
                <option>Storm</option>
            </select>
            <label>Describe your area</label>
            <input id="q2" placeholder="Example: heavy rain near my house">
            <button onclick="buildPrompt('disaster')">Generate Guided Prompt</button>
        `;
        prompt = "There is a disaster or emergency situation.";
    }

    if (type === "privacy") {
        html = `
            <h3>🔒 Privacy Leak</h3>
            <label>Paste the text containing sensitive information</label>
            <input id="q1" placeholder="Example: phone, Aadhaar, PAN, email">
            <button onclick="buildPrompt('privacy')">Generate Guided Prompt</button>
        `;
        prompt = "I need help checking and masking sensitive information.";
    }

    if (type === "sos") {
        html = `
            <h3>🆘 SOS Message Generator</h3>
            <label>What is happening?</label>
            <input id="q1" placeholder="Example: I am unsafe / fire / flood / medical help">
            <label>Who should receive the message?</label>
            <input id="q2" placeholder="Example: family, friend, emergency contact">
            <button onclick="buildPrompt('sos')">Generate Guided Prompt</button>
        `;
        prompt = "I need an emergency SOS message.";
    }

    box.innerHTML = html;
    input.value = prompt;
}

function startVoiceInput() {
    const input = document.getElementById("userInput");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Voice input is not supported in this browser. Please use Chrome.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onstart = function () {
        input.placeholder = "Listening...";
    };

    recognition.onresult = function (event) {
        const speechText = event.results[0][0].transcript;
        input.value = input.value + " " + speechText;
        input.placeholder = "Your guided situation will appear here. You can also type extra details...";
    };

    recognition.onerror = function () {
        alert("Voice input failed. Please try again.");
        input.placeholder = "Your guided situation will appear here. You can also type extra details...";
    };
}

function buildPrompt(type) {
    const input = document.getElementById("userInput");

    if (type === "scam") {
        input.value =
            `Scam/Fraud situation: ${document.getElementById("q1").value}. ` +
            `It asked for OTP/password/KYC: ${document.getElementById("q2").value}.`;
    }

    if (type === "women") {
        const alone = document.getElementById("q1").value.toLowerCase();
        const danger = document.getElementById("q2").value.toLowerCase();
        const location = document.getElementById("q3").value;

        input.value =
            `women_safety_report alone=${alone} ` +
            `following=${danger === "yes" ? "yes" : danger === "no" ? "no" : "unknown"} ` +
            `harassing=${danger === "yes" ? "yes" : danger === "no" ? "no" : "unknown"} ` +
            `location=${location}`;
    }

    if (type === "medical") {
        input.value =
            `Medical emergency: ${document.getElementById("q1").value}. ` +
            `Person conscious: ${document.getElementById("q2").value}.`;
    }

    if (type === "disaster") {
        input.value =
            `Disaster situation: ${document.getElementById("q1").value}. ` +
            `Area details: ${document.getElementById("q2").value}.`;
    }

    if (type === "privacy") {
        input.value =
            `Privacy leak situation. Please detect and mask sensitive information: ${document.getElementById("q1").value}.`;
    }

    if (type === "sos") {
        input.value =
            `SOS request: ${document.getElementById("q1").value}. ` +
            `Generate emergency message for: ${document.getElementById("q2").value}.`;
    }
}

function listItems(value) {
    if (!value) return "";

    // Case 1: normal array
    if (Array.isArray(value)) {
        return value.map(item => {
            if (typeof item === "object" && item !== null) {
                if (item.name && item.number) {
                    return `<li>${item.name} — ${item.number}</li>`;
                }
                return `<li>${JSON.stringify(item)}</li>`;
            }

            return `<li>${item}</li>`;
        }).join("");
    }

    // Case 2: MCP emergency contacts object
    if (value.contacts && Array.isArray(value.contacts)) {
        return value.contacts
            .map(contact => `<li>${contact.name} — ${contact.number}</li>`)
            .join("");
    }

    // Case 3: MCP disaster plan object
    if (value.plan && Array.isArray(value.plan)) {
        return value.plan
            .map(item => `<li>${item}</li>`)
            .join("");
    }

    // Case 4: fallback for any object/string
    if (typeof value === "object") {
        return `<li>${JSON.stringify(value)}</li>`;
    }

    return `<li>${value}</li>`;
}

function safeText(value, fallback = "Not available.") {
    return value || fallback;
}

function getRiskColor(risk) {
    if (risk === "High") return "#ef4444";
    if (risk === "Medium") return "#f59e0b";
    return "#22c55e";
}

function renderRiskCard(risk, score) {
    return `
        <div class="card">
            <h2>Risk Assessment</h2>
            <div class="risk" style="background:${getRiskColor(risk)}">
                ${risk || "Unknown"} ${score !== undefined ? `(${score}/100)` : ""}
            </div>
        </div>
    `;
}

function renderThreat(threat) {
    return `
        ${renderRiskCard(threat.risk_level, threat.risk_score)}

        <div class="card">
            <h2>Threat Type</h2>
            <p>${safeText(threat.threat_type)}</p>
        </div>

        <div class="card">
            <h2>Situation Summary</h2>
            <p>${safeText(threat.situation_summary)}</p>
        </div>

        <div class="card">
            <h2>Why This Is Risky</h2>
            <p>${safeText(threat.why_this_is_risky)}</p>
        </div>

        <div class="card">
            <h2>Warning Signs</h2>
            <ul>${listItems(threat.warning_signs)}</ul>
        </div>

      
       ${threat.mcp_verification ? `
    <div class="card">
        <h2>🔧 MCP Scam Verification</h2>

        <h3>Matched Scam Indicators</h3>
        <ul>
            ${listItems(threat.mcp_verification.matched_warning_signs)}
        </ul>

        <h3>Tool Advice</h3>
        <p>${safeText(threat.mcp_verification.tool_advice)}</p>

        <h3>Tool Used</h3>
        <p>${safeText(threat.mcp_verification.tool)}</p>
    </div>
` : ""}
    </ul>

        <div class="card">
            <h2>Recommended Actions</h2>
            <ul>${listItems(threat.recommended_actions)}</ul>
        </div>

        <div class="card">
            <h2>Safe Reply</h2>
            <p>${safeText(threat.safe_reply)}</p>
        </div>

        <div class="card">
            <h2>Security Tips</h2>
            <ul>${listItems(threat.security_tips)}</ul>
        </div>
    `;
}

function renderPersonalSafety(safety) {
    return `
        ${renderRiskCard(safety.risk_level, safety.risk_score)}

        <div class="card">
            <h2>Situation Summary</h2>
            <p>${safeText(safety.situation_summary)}</p>
        </div>

        <div class="card">
            <h2>Why This Is Risky</h2>
            <p>${safeText(safety.why_this_is_risky)}</p>
        </div>

        <div class="card">
            <h2>Next 5 Minutes</h2>
            <ul>${listItems(safety.next_5_minutes)}</ul>
        </div>

        <div class="card">
            <h2>Next 30 Minutes</h2>
            <ul>${listItems(safety.next_30_minutes)}</ul>
        </div>

        <div class="card">
            <h2>SOS Message</h2>
            <p>${safeText(safety.custom_sos_message)}</p>
        </div>

        <div class="card">
            <h2>Emergency Contacts</h2>
            <ul>${listItems(safety.emergency_contacts)}</ul>
        </div>

        <div class="card">
            <h2>Safety Tips</h2>
            <ul>${listItems(safety.safety_tips)}</ul>
        </div>
    `;
}

function renderPrivacy(privacy) {
    return `
        <div class="card">
            <h2>Privacy Scan</h2>
            <p><strong>Detected Items:</strong> ${privacy.detected_count}</p>
            <p><strong>Masked Text:</strong> ${privacy.masked_text}</p>
        </div>
    `;
}

function renderCrisis(crisis, plan) {
    let html = "";

    if (crisis) {
        html += `
            ${renderRiskCard(crisis.risk_level, crisis.risk_score)}

            <div class="card">
                <h2>Crisis Type</h2>
                <p>${safeText(crisis.crisis_type)}</p>
            </div>

            <div class="card">
                <h2>Situation Summary</h2>
                <p>${safeText(crisis.situation_summary)}</p>
            </div>

            <div class="card">
                <h2>Why This Is Risky</h2>
                <p>${safeText(crisis.why_this_is_risky)}</p>
            </div>

            <div class="card">
                <h2>Danger Signs</h2>
                <ul>${listItems(crisis.danger_signs)}</ul>
            </div>

            <div class="card">
                <h2>Recommended Priority</h2>
                <p>${safeText(crisis.recommended_priority)}</p>
            </div>

            <div class="card">
                <h2>Emergency Contacts</h2>
                <ul>${listItems(crisis.emergency_contacts)}</ul>
            </div>
        `;
    }

    if (plan) {
        html += `
            <div class="card">
                <h2>Immediate Action Plan</h2>
                <ul>${listItems(plan.immediate_plan)}</ul>
            </div>

            <div class="card">
                <h2>Next 30 Minutes</h2>
                <ul>${listItems(plan.next_30_minutes)}</ul>
            </div>

            <div class="card">
                <h2>Emergency Kit</h2>
                <ul>${listItems(plan.emergency_kit)}</ul>
            </div>

            <div class="card">
                <h2>Avoid</h2>
                <ul>${listItems(plan.avoid)}</ul>
            </div>

            <div class="card">
                <h2>Family Safety Message</h2>
                <p>${safeText(plan.safe_message)}</p>
            </div>
            ${plan.mcp_plan ? `
    <div class="card">
        <h2>🔧 MCP ${plan.crisis_type} Response Plan</h2>
        <ul>${listItems(plan.mcp_plan)}</ul>
    </div>
` : ""}
        `;
    }

    return html;
}
function renderEmotionalSupport(support) {
    return `
        <div class="card emotional-card">
            <h2>💙 Emotional Support Available</h2>
            <p><strong>${safeText(support.opening_message)}</strong></p>
            <p>${safeText(support.empathetic_response)}</p>
            <p>${safeText(support.follow_up_question)}</p>

            <button class="chat-btn" onclick="openEmotionalChat()">
                Talk to SafeSphere
            </button>
            <button class="not-now-btn" onclick="closeEmotionalChat()">
                Not Now
            </button>
        </div>

        <div id="emotionalChatBox" class="chat-box" style="display:none;">
            <h3>💙 SafeSphere Companion</h3>
            <div id="chatMessages" class="chat-messages">
                <div class="bot-msg">${safeText(support.opening_message)}</div>
                <div class="bot-msg">${safeText(support.follow_up_question)}</div>
            </div>

            <div class="chat-input-row">
                <input id="chatInput" placeholder="Type what you're feeling...">
                <button onclick="sendEmotionalMessage()">Send</button>
            </div>
        </div>
    `;
}

function openEmotionalChat() {
    document.getElementById("emotionalChatBox").style.display = "block";
}

function closeEmotionalChat() {
    document.getElementById("emotionalChatBox").style.display = "none";
}

async function sendEmotionalMessage() {
    const input = document.getElementById("chatInput");
    const messages = document.getElementById("chatMessages");

    const userText = input.value.trim();
    if (!userText) return;

    messages.innerHTML += `<div class="user-msg">${userText}</div>`;
    input.value = "";

    messages.innerHTML += `<div class="bot-msg">Typing...</div>`;

    try {
        const response = await fetch("http://127.0.0.1:5000/emotional-chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: userText})
        });

        const data = await response.json();

        const typingMsg = messages.querySelector(".bot-msg:last-child");
        typingMsg.innerText = data.reply || "I'm here with you. Tell me more.";
    } catch (error) {
        const typingMsg = messages.querySelector(".bot-msg:last-child");
        typingMsg.innerText = "I'm here with you. You can tell me more.";
    }
}
async function analyzeSafety() {
    const input = document.getElementById("userInput").value;
    const resultDiv = document.getElementById("result");

    if (!input.trim()) {
        resultDiv.innerHTML = "<p>Please enter a safety situation.</p>";
        return;
    }

    resultDiv.innerHTML = "<p>Analyzing with SafeSphere AI...</p>";

    try {
        const response = await fetch("http://127.0.0.1:5000/safe-sphere", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({input: input})
        });

        const data = await response.json();
        console.log("FULL BACKEND DATA:", data);

        const final = data.final_response || {};
        let html = "";
        if (final.emotional_support) {
        html += renderEmotionalSupport(final.emotional_support);
        }

        if (final.threat_analysis) {
            html += renderThreat(final.threat_analysis);
        }

        if (final.personal_safety) {
            html += renderPersonalSafety(final.personal_safety);
        }

        if (final.privacy_scan) {
            html += renderPrivacy(final.privacy_scan);
        }

        if (final.crisis_assessment || final.action_plan) {
            html += renderCrisis(final.crisis_assessment, final.action_plan);
        }

        if (data.explanation) {
            html += `
                <div class="card">
                    <h2>AI Final Advice</h2>
                    <p>${safeText(data.explanation.final_advice)}</p>
                </div>

                <div class="card">
                    <h2>What To Do Now</h2>
                    <ul>${listItems(data.explanation.what_to_do_now)}</ul>
                </div>

                <div class="card">
                    <h2>Important Note</h2>
                    <p>${safeText(data.explanation.important_note)}</p>
                </div>
            `;
        }

        if (!html) {
            html = `
                <div class="card">
                    <h2>SafeSphere Response</h2>
                    <p>No specific agent response found.</p>
                </div>
            `;
        }

        html += `
            <div class="card">
                <h2>Agents Used</h2>
                <ul>${listItems(data.selected_agents)}</ul>
            </div>

            <div class="card">
                <h2>Summary</h2>
                <p>${safeText(data.explanation?.short_summary || data.summary)}</p>
            </div>
        `;

        resultDiv.innerHTML = html;

    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = `<p>Frontend display error: ${error.message}</p>`;
    }
}