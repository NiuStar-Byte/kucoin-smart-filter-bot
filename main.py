import time
import os
from kucoin_data import fetch_ohlcv
from smart_filter import SmartFilter
from telegram_alert import send_alert

TOKENS = [
    "SUIUSDTM", "OPUSDTM", "ARBUSDTM", "DOGEUSDTM", "XRPUSDTM",
    "LINKUSDTM", "BCHUSDTM", "LTCUSDTM", "DOTUSDTM", "MATICUSDTM",
    "SOLUSDTM", "ATOMUSDTM", "AVAXUSDTM", "APTUSDTM", "RNDRUSDTM",
    "PEPEUSDTM", "TIAUSDTM", "SEIUSDTM", "FETUSDTM", "WLDUSDTM"
]

INTERVAL = int(os.getenv("INTERVAL_MINUTES", 3))  # interval in minutes
TIMEFRAMES = ["2min", "3min", "5min"]

def run():
    for symbol in TOKENS:
        for tf in TIMEFRAMES:
            try:
                df = fetch_ohlcv(symbol, interval=tf)
                if df is not None:
                    result = SmartFilter(symbol, df, tf).analyze()
                    if result and not os.getenv("DRY_RUN", "false").lower() == "true":
                        send_alert(result)
            except Exception as e:
                print(f"[{symbol} {tf}] Unexpected error:", e)

if __name__ == "__main__":
    print(f"📡 Auto Scheduler Started | Interval: {INTERVAL} minutes")
    while True:
        run()
        print(f"✅ Cycle complete. Sleeping {INTERVAL} minutes...\n")
        time.sleep(INTERVAL * 60)
