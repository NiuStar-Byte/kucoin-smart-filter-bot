from kucoin_data import fetch_ohlcv
from smart_filter import SmartFilter
from telegram_alert import send_alert
import os

TOKENS = [
    "SUIUSDTM", "SKATEUSDTM", "SPARKUSDTM", "LAUSDTM", "BIDUSDTM",
    "SPKUSDTM", "ZKJUSDTM", "IPUSDTM", "AEROUSDTM", "BMTUSDTM",
    "LQTYUSDTM", "FUNUSDTM", "SNTUSDTM", "XUSDTM", "BANKUSDTM",
    "RAYUSDTM", "REXUSDTM", "EPTUSDTM", "ELDEUSDTM", "MAGICUSDTM"
]

def run():
    for symbol in TOKENS:
        df = fetch_ohlcv(symbol)
        if df is not None:
            result = SmartFilter(symbol, df).analyze()
            if result and not os.getenv("DRY_RUN", "false").lower() == "true":
                send_alert(result)

if __name__ == "__main__":
    run()
