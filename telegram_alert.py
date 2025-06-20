# telegram_alert.py
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_alert(result):
    symbol = result.get("symbol")
    signal = result.get("signal")
    price = result.get("price")
    score = result.get("score")
    confirmed_timeframes = result.get("confirmed_timeframes", "")

    message = (
        f"[{symbol}] Signal \u2192 {('📈 LONG' if signal == 'LONG' else '📉 SHORT')} Signal\n"
        f"Price: {price}\n"
        f"Score: {score}/100\n"
        f"Confirmed on: {confirmed_timeframes}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if not response.ok:
            print("Failed to send alert:", response.text)
    except Exception as e:
        print("Exception in send_alert:", e)
