import time
from kucoin_data import fetch_klines
from smart_filter import SmartFilter
from telegram_alert import send_telegram_alert

TOKENS = [
    "SUIUSDTM", "SKATEUSDTM", "BIDUSDTM", "LAUSDTM", "SPARKUSDTM",
    "SPKUSDTM", "ZKJUSDTM", "IPUSDTM", "AEROUSDTM", "BMTUSDTM",
    "LQTYUSDTM", "FUNUSDTM", "SNTUSDTM", "XUSDTM", "BANKUSDTM",
    "RAYUSDTM", "REXUSDTM", "EPTUSDTM", "ELDEUSDTM", "MAGICUSDTM",
    "ACTUSDTM", "OPUSDTM", "ARBUSDTM", "DOGEUSDTM", "XRPUSDTM",
    "LINKUSDTM", "BCHUSDTM", "LTCUSDTM", "DOTUSDTM", "MATICUSDTM",
    "SOLUSDTM", "ATOMUSDTM", "AVAXUSDTM", "APTUSDTM", "RNDRUSDTM",
    "PEPEUSDTM", "TIAUSDTM", "SEIUSDTM", "FETUSDTM", "WLDUSDTM"
]

TIMEFRAMES = ["2min", "3min", "5min"]
INTERVAL_MAP = {
    "2min": 2,
    "3min": 3,
    "5min": 5
}

def run():
    while True:
        for token in TOKENS:
            for tf in TIMEFRAMES:
                try:
                    interval = INTERVAL_MAP[tf]
                    df = fetch_klines(token, interval)
                    if df is None or df.empty:
                        print(f"[{token} {tf}] Data error or empty.")
                        continue

                    sf = SmartFilter(token, df)
                    signal = sf.analyze()

                    if signal:
                        send_telegram_alert(f"[{token} {tf}] Signal → 📈 {signal}" if "LONG" in signal else f"[{token} {tf}] Signal → 📉 {signal}")
                    else:
                        print(f"[{token} {tf}] ❌ No Signal")

                except Exception as e:
                    print(f"[{token} {tf}] Unexpected error: {e}")

        print("✅ Cycle complete. Sleeping 3 minutes...\n")
        time.sleep(180)

if __name__ == "__main__":
    run()
