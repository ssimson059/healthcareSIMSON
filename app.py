import os
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder="static", static_url_path="")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

DOMAIN_NAME = "Healthcare"
SYSTEM_PROMPT = (
    "You are a helpful assistant that ONLY answers questions related to healthcare, medical symptoms (general info only, not diagnosis), hospital services, appointments, health insurance basics, and wellness. "
    "If the user asks something unrelated to this domain, politely say you can only help with "
    f"{DOMAIN_NAME} related questions and ask them to rephrase within that scope. "
    "Keep answers clear, concise, and friendly. "
    "This assistant gives general health information only and is not a substitute for professional medical advice."
)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    if not GEMINI_API_KEY:
        return jsonify({
            "reply": "Server is missing GEMINI_API_KEY. Add it to your .env file and restart the server."
        }), 500

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": user_message}]}
        ]
    }

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()
        reply = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Sorry, I could not generate a response.")
        )
    except Exception as exc:
        reply = f"Error contacting Gemini API: {exc}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
