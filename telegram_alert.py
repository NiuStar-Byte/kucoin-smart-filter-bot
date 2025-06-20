import os
import requests

def send_alert(message):
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not bot_token or not chat_id:
        print("Missing BOT_TOKEN or CHAT_ID environment variable.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            print("Failed to send alert:", resp.text)
    except Exception as e:
        print("Exception while sending alert:", e)

