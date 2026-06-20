from flask import Flask, request
import os
import json
from datetime import datetime
from services.webhook_service import save_webhook
from utils.logger import logger
import json

app = Flask(__name__)

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

    logger.info(
    f"Webhook received | timestamp={timestamp}"
    )

    try:
        payload = request.get_json()

        logger.info(f"Incoming Webhook Payload: {json.dumps(payload, indent=2)}")

        webhook_id = save_webhook(payload)

        logger.info(f"Webhook saved successfully | ID: {webhook_id}")

    except Exception as e:
        logger.error(f"Webhook processing failed | Error: {e}")
        try:
            logger.info(f"Raw Payload: {request.data.decode('utf-8')}")
        except:
            pass

    logger.info("====================================")
    return "", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5003))
    print(f"\nListening on port {port}\n")
    app.run(host="0.0.0.0", port=port)
