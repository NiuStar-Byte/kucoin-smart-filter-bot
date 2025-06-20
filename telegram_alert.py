import requests
import os

# Your actual bot token and chat ID (secured from environment or hardcoded)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7100609549:AAHmeFe0RondzYyPKNuGTTp8HNAuT0PbNJs")
CHAT_ID = os.getenv("CHAT_ID", "-1002857433223")  # Group: AlterEgoTalinNius

def send_telegram_alert(symbol, signal_type, price, tf, score, passed, required):
    try:
        stack_result = (
            f"📊 <b>{symbol} {tf}</b>\n"
            f"✅ Signal: <b>{signal_type.upper()}</b>\n"
            f"💰 Price: <code>{price}</code>\n"
            f"🎯 Score: <code>{score}/18</code>\n"
            f"📌 Required Passed: <code>{passed}/12</code>\n"
        )

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": stack_result,
                "parse_mode": "HTML"
            }
        )

        if not response.ok:
            print(f"❌ Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"❌ Telegram alert error: {e}")
