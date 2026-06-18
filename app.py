from flask import Flask, request
import os
import json
from datetime import datetime
from services.webhook_service import save_webhook

app = Flask(__name__)

# Set port and verify token
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "Govardhan")


@app.route("/", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return challenge, 200

    return "", 403


@app.route("/", methods=["POST"])
def receive_webhook():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n\nWebhook received {timestamp}\n")

    try:
        print(json.dumps(request.get_json(), indent=2))
    except Exception:
        print(request.data.decode("utf-8"))

    return "", 200

@app.route("/", methods=["POST"])
def receive_webhook():
    try:
        payload = request.get_json()

        webhook_id = save_webhook(payload)

        print(f"Webhook saved: {webhook_id}")

    except Exception as e:
        print(f"Error saving webhook: {e}")

    return "", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5003))
    print(f"\nListening on port {port}\n")
    app.run(host="0.0.0.0", port=port)
