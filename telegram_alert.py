import os
import requests

def send_alert(result):
    try:
        message, score, stacks, df, symbol, interval = result

        detail_lines = [f"📊 *{symbol}* `{interval}` — Score: *{score}/18*"]
        for k, v in stacks.items():
            emoji = "✅" if v else "❌"
            detail_lines.append(f"{emoji} `{k}`")

        price = df['close'].iloc[-1]
        trend = "📈" if "LONG" in message else "📉"

        final_text = (
            f"{trend} *{message}*\n"
            f"Price: `{price}`\n"
            f"{chr(10).join(detail_lines)}"
        )

        payload = {
            "chat_id": os.environ.get("CHAT_ID"),
            "text": final_text,
            "parse_mode": "Markdown"
        }

        resp = requests.post(
            f"https://api.telegram.org/bot{os.environ.get('BOT_TOKEN')}/sendMessage",
            json=payload
        )

        if resp.status_code != 200:
            print(f"Failed to send alert: {resp.text}")
        else:
            print(f"✅ Telegram alert sent for {symbol} ({interval})")

    except Exception as e:
        print(f"❌ Telegram alert error: {e}")
