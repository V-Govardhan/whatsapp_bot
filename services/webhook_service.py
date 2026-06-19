from datetime import datetime
from config.database import webhooks_collection


def save_webhook(payload):

    value = payload.get("entry", [{}])[0] \
                   .get("changes", [{}])[0] \
                   .get("value", {})

    document = {
        "received_at": datetime.utcnow()
    }


    # =========================
    # RECEIVED MESSAGE WEBHOOK
    # =========================

    if "messages" in value:

        message = value["messages"][0]

        contact = value.get("contacts", [{}])[0]
        metadata = value.get("metadata", {})

        document.update({

            "webhook_type": "received",

            "from_number": message.get("from"),
            "to_number": metadata.get("display_phone_number"),

            "profile_name": contact
                .get("profile", {})
                .get("name"),

            "wa_id": contact.get("wa_id"),

            "message_id": message.get("id"),

            "message_type": message.get("type"),

            "message_timestamp":
                datetime.fromtimestamp(
                    int(message.get("timestamp"))
                )
        })


        # text message
        if message.get("type") == "text":

            document["message"] = (
                message
                .get("text", {})
                .get("body")
            )

        else:
            document["message"] = None



    # =========================
    # STATUS WEBHOOK
    # sent/delivered/read
    # =========================

    elif "statuses" in value:

        status = value["statuses"][0]


        # WhatsApp gives:
        # sent / delivered / read / failed

        document.update({

            "webhook_type": status.get("status"),

            "message_id": status.get("id"),

            "to_number": status.get(
                "recipient_id"
            ),

            "status_timestamp":
                datetime.fromtimestamp(
                    int(status.get("timestamp"))
                )
        })


        # failed reason
        if status.get("status") == "failed":

            document["error"] = status.get(
                "errors",
                []
            )


    # =========================
    # FALLBACK
    # =========================

    else:

        document.update({

            "webhook_type": "unknown",

            "payload": payload
        })


    result = webhooks_collection.insert_one(document)

    return str(result.inserted_id)