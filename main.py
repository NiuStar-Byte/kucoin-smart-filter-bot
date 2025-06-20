# main.py
from kucoin_data import fetch_ohlcv
from smart_filter import SmartFilter
from telegram_alert import send_alert
import os

TOKENS = [
    "SUIUSDTM", "OPUSDTM", "ARBUSDTM", "DOGEUSDTM", "XRPUSDTM",
    "LINKUSDTM", "BCHUSDTM", "LTCUSDTM", "DOTUSDTM", "MATICUSDTM",
    "SOLUSDTM", "ATOMUSDTM", "AVAXUSDTM", "APTUSDTM", "RNDRUSDTM",
    "PEPEUSDTM", "TIAUSDTM", "SEIUSDTM", "FETUSDTM", "WLDUSDTM"
]

TIMEFRAMES = ["2m", "3m", "5m"]

def run():
    for symbol in TOKENS:
        signals = []
        for tf in TIMEFRAMES:
            df = fetch_ohlcv(symbol, interval=tf)
            if df is not None:
                result = SmartFilter(symbol, df).analyze()
                if (
                    result and
                    result.get("signal") and
                    result.get("required_passed")
                ):
                    signals.append((tf, result))

        if len(signals) >= 2:  # Require at least 2 timeframes to agree
            tf_list = ", ".join([s[0] for s in signals])
            base_result = signals[0][1]
            base_result["confirmed_timeframes"] = tf_list
            if not os.getenv("DRY_RUN", "false").lower() == "true":
                send_alert(base_result)

if __name__ == "__main__":
    run()
