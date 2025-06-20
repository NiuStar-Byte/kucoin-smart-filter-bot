from kucoin_data import fetch_ohlcv
from smart_filter import SmartFilter
from telegram_alert import send_alert
import os
import time

TOKENS = [
    "SUIUSDTM", "OPUSDTM", "ARBUSDTM", "DOGEUSDTM", "XRPUSDTM",
    "LINKUSDTM", "BCHUSDTM", "LTCUSDTM", "DOTUSDTM", "MATICUSDTM",
    "SOLUSDTM", "ATOMUSDTM", "AVAXUSDTM", "APTUSDTM", "RNDRUSDTM",
    "PEPEUSDTM", "TIAUSDTM", "SEIUSDTM", "FETUSDTM", "WLDUSDTM"
]

INTERVALS = {
    "2min": "2min",
    "3min": "3min",
    "5min": "5min"
}

COOLDOWNS = {
    "2min": 300,   # 5 minutes
    "3min": 720,   # 12 minutes
    "5min": 900    # 15 minutes (default/fallback)
}

last_alert_time = {}

def run():
    for interval_label, interval_value in INTERVALS.items():
        for symbol in TOKENS:
            key = f"{symbol}_{interval_label}"
            now = time.time()

            if key in last_alert_time and now - last_alert_time[key] < COOLDOWNS[interval_label]:
                continue  # Skip due to cooldown

            df = fetch_ohlcv(symbol, interval=interval_value, limit=150)

            if df is not None:
                try:
                    result = SmartFilter(symbol, df, interval_label).analyze()
                    if result and not os.getenv("DRY_RUN", "false").lower() == "true":
                        send_alert(result)
                        last_alert_time[key] = now
                except Exception as e:
                    print(f"[{symbol} {interval_label}] Unexpected error: {e}")

    print("✅ Cycle complete. Sleeping 3 minutes...")
    time.sleep(180)

if __name__ == "__main__":
    while True:
        run()
