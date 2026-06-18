from datetime import datetime
from config.database import webhooks_collection


def save_webhook(payload):
    document = {
        "received_at": datetime.utcnow(),
        "payload": payload
    }

    result = webhooks_collection.insert_one(document)

    return str(result.inserted_id)
