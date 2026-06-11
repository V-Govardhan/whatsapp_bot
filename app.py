from flask import Flask, request
import os
import json
from datetime import datetime

app = Flask(__name__)

VERIFY_TOKEN = "vibecode"

@app.route("/", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    token = request.args.get("hub.verify_token")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return challenge, 200

    return {
        "mode": mode,
        "token": token,
        "status": "verification failed"
    }, 403


@app.route("/", methods=["POST"])
def webhook():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nWebhook received {timestamp}\n")
    print(json.dumps(request.json, indent=2))

    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
