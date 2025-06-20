import pandas as pd

class SmartFilter:
    def __init__(self, symbol, df):
        self.symbol = symbol
        self.df = df

    def analyze(self):
        try:
            if self.df is None or self.df.empty:
                return None

            # Normalize columns
            self.df.columns = [col.lower() for col in self.df.columns]
            self.df = self.df.dropna()
            if len(self.df) < 20:
                return None

            score = 0
            total_stacks = 5

            close = self.df['close']
            high = self.df['high']
            low = self.df['low']

            ### 1. Fractal Zones (Structure Confirm)
            fractal_bull = close.iloc[-1] > max(close[-5:-1])
            fractal_bear = close.iloc[-1] < min(close[-5:-1])
            if fractal_bull:
                score += 1
            elif fractal_bear:
                score -= 1

            ### 2. Fibonacci Vortex (Retracement Logic)
            high20 = high[-20:].max()
            low20 = low[-20:].min()
            retrace = (close.iloc[-1] - low20) / (high20 - low20 + 1e-9)
            if retrace > 0.618:
                score += 1
            elif retrace < 0.382:
                score -= 1

            ### 3. MACD Dynamic Signal
            ema12 = close.ewm(span=12).mean()
            ema26 = close.ewm(span=26).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9).mean()
            macd_cross = macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]
            macd_cross_down = macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]
            if macd_cross:
                score += 1
            elif macd_cross_down:
                score -= 1

            ### 4. Quantum Momentum (UST logic)
            momentum = close.pct_change().rolling(5).mean().iloc[-1]
            if momentum > 0.004:
                score += 1
            elif momentum < -0.004:
                score -= 1

            ### 5. EMA Cloud + HATS
            ema50 = close.ewm(span=50).mean()
            ema100 = close.ewm(span=100).mean()
            cloud_bias = ema50.iloc[-1] > ema100.iloc[-1]
            cloud_cross = ema50.iloc[-2] < ema100.iloc[-2] and cloud_bias
            cloud_cross_down = ema50.iloc[-2] > ema100.iloc[-2] and not cloud_bias
            if cloud_cross:
                score += 1
            elif cloud_cross_down:
                score -= 1

            # Final Score Evaluation
            if score >= 3:
                signal = f"📈 LONG Signal for {self.symbol} at {close.iloc[-1]:.4f}"
            elif score <= -3:
                signal = f"📉 SHORT Signal for {self.symbol} at {close.iloc[-1]:.4f}"
            else:
                return None  # No valid signal

            return signal

        except Exception as e:
            print(f"[{self.symbol}] Error in SmartFilter: {e}")
            return None
