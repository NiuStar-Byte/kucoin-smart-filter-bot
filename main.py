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

def run():
    for symbol in TOKENS:
        df = fetch_ohlcv(symbol)
        if df is not None:
            result = SmartFilter(symbol, df).analyze()
            if (
                result and
                result.get("signal") and
                result.get("required_passed")
            ):
                if not os.getenv("DRY_RUN", "false").lower() == "true":
                    send_alert(result)

if __name__ == "__main__":
    run()
