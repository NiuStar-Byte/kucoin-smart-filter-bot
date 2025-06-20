import os
import time
from kucoin_data import fetch_ohlcv
from smart_filter import SmartFilter
from telegram_alert import send_telegram_alert

TOKENS = [
    "SUIUSDTM", "OPUSDTM", "ARBUSDTM", "DOGEUSDTM", "XRPUSDTM",
    "LINKUSDTM", "BCHUSDTM", "LTCUSDTM", "DOTUSDTM", "MATICUSDTM",
    "SOLUSDTM", "ATOMUSDTM", "AVAXUSDTM", "APTUSDTM", "RNDRUSDTM",
    "PEPEUSDTM", "TIAUSDTM", "SEIUSDTM", "FETUSDTM", "WLDUSDTM"
]

TIMEFRAMES = ["2min", "3min", "5min"]
COOLDOWN = {
    "2min": 300,   # 5 minutes
    "3min": 720,   # 12 minutes
    "5min": 900    # 15 minutes
}
last_sent = {}

def run():
    for symbol in TOKENS:
        for tf in TIMEFRAMES:
            key = f"{symbol}_{tf}"
            now = time.time()
            if key in last_sent and (now - last_sent[key]) < COOLDOWN[tf]:
                continue

            try:
                df = fetch_ohlcv(symbol, tf)
                if df is not None:
                    filter = SmartFilter(symbol, df, min_score=9, required_passed=7, tf=tf)
                    result = filter.analyze()
                    if result:
                        if os.getenv("DRY_RUN", "false").lower() != "true":
                            send_telegram_alert(symbol, result.split()[0], df['close'].iloc[-1], tf, filter.total_score, sum(filter.stack_results.values()))
                        last_sent[key] = now
            except Exception as e:
                print(f"[{symbol} {tf}] Unexpected error: {e}")

    print("✅ Cycle complete. Sleeping 3 minutes...\n")

if __name__ == "__main__":
    run()
