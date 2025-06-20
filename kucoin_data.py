import requests
import pandas as pd

def fetch_ohlcv(symbol, interval='1min', limit=150):
    url = f"https://api-futures.kucoin.com/api/v1/kline/query?symbol={symbol}&granularity=60&limit={limit}"
    try:
        resp = requests.get(url)
        data = resp.json().get("data", [])
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "close", "high", "low", "volume", "turnover"
        ])
        df = df.astype(float)
        return df
    except Exception as e:
        print(f"[{symbol}] Error fetching data:", e)
        return None
