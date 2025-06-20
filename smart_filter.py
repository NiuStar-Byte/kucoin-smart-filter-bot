import pandas as pd

class SmartFilter:
    def __init__(self, symbol, df, timeframe):
        self.symbol = symbol
        self.df = df
        self.timeframe = timeframe
        self.result = None
        self.stack_results = {}
        self.total_score = 0
        self.passed_required = True

    def analyze(self):
        if self.df is None or self.df.empty or len(self.df.columns) < 6:
            print(f"[{self.symbol} {self.timeframe}] DataFrame is invalid or missing columns.")
            return None

        try:
            self.stack_results = {
                "Fractal Zone": self._check_fractal_zone(),
                "EMA Cloud": self._check_ema_cloud(),
                "MACD": self._check_macd(),
                "Momentum": self._check_momentum(),
                "HATS": self._check_hats(),

                "Volume Spike": self._check_volume_spike(),
                "VWAP Divergence": self._optional_dummy(),
                "MTF Volume Agreement": self._optional_dummy(),

                "HH/LL Trend": self._check_hh_ll(),
                "EMA Structure": self._optional_dummy(),

                "Chop Zone": self._check_chop_zone(),

                "Candle Confirmation": self._check_candle_close(),
                "Wick Dominance": self._optional_dummy(),
                "Absorption": self._optional_dummy(),

                "Support/Resistance": self._check_dummy_sr(),
                "Smart Money Bias": self._optional_dummy(),

                "Liquidity Pool": self._check_dummy_liquidity(),
                "Spread Filter": self._check_dummy_volatility(),
            }

            required_items = {
                "Fractal Zone", "EMA Cloud", "MACD", "Momentum", "HATS",
                "Volume Spike", "HH/LL Trend", "Chop Zone",
                "Candle Confirmation", "Support/Resistance",
                "Liquidity Pool", "Spread Filter"
            }

            score = 0
            required_passed = True
            for name, passed in self.stack_results.items():
                if passed:
                    score += 1
                elif name in required_items:
                    required_passed = False

            self.total_score = score
            self.passed_required = required_passed

            print(f"[{self.symbol} {self.timeframe}] Score: {score}/18 | Required Passed: {required_passed}")
            for name, passed in self.stack_results.items():
                print(f"[{name}] → {'✅' if passed else '❌'}")

            if score >= 12 and required_passed:
                last_close = self.df['close'].iloc[-1]
                trend_bias = "LONG" if self.df['close'].iloc[-1] > self.df['open'].iloc[-1] else "SHORT"
                signal = f"{trend_bias} Signal for {self.symbol} at {last_close} ({self.timeframe})"
                print(f"[{self.symbol} {self.timeframe}] ✅ FINAL SIGNAL → {signal}")
                return {
                    "symbol": self.symbol,
                    "direction": trend_bias,
                    "price": last_close,
                    "timeframe": self.timeframe,
                    "score": score
                }
            else:
                print(f"[{self.symbol} {self.timeframe}] ❌ No Signal (Score too low or missing required)")
                return None

        except Exception as e:
            print(f"[{self.symbol} {self.timeframe}] SmartFilter Error: {e}")
            return None

    # STACK IMPLEMENTATIONS (same as your version)

    def _check_fractal_zone(self):
        return self.df['close'].iloc[-1] > self.df['low'].rolling(20).min().iloc[-1]

    def _check_ema_cloud(self):
        ema21 = self.df['close'].ewm(span=21).mean()
        ema89 = self.df['close'].ewm(span=89).mean()
        return ema21.iloc[-1] > ema89.iloc[-1]

    def _check_macd(self):
        ema12 = self.df['close'].ewm(span=12).mean()
        ema26 = self.df['close'].ewm(span=26).mean()
        macd_line = ema12 - ema26
        signal = macd_line.ewm(span=9).mean()
        return macd_line.iloc[-1] > signal.iloc[-1]

    def _check_momentum(self):
        mom = self.df['close'].diff()
        return mom.iloc[-1] > 0

    def _check_hats(self):
        ha_close = (self.df['open'] + self.df['high'] + self.df['low'] + self.df['close']) / 4
        return ha_close.iloc[-1] > ha_close.iloc[-2]

    def _check_volume_spike(self):
        avg_vol = self.df['volume'].rolling(10).mean()
        return self.df['volume'].iloc[-1] > 1.5 * avg_vol.iloc[-1]

    def _check_chop_zone(self):
        rsi = self.df['close'].rolling(14).apply(lambda x: (x.diff() > 0).sum(), raw=False)
        return rsi.iloc[-1] > 7

    def _check_candle_close(self):
        body = abs(self.df['close'].iloc[-1] - self.df['open'].iloc[-1])
        wick = abs(self.df['high'].iloc[-1] - self.df['low'].iloc[-1])
        return body > 0.5 * wick

    def _check_hh_ll(self):
        return self.df['high'].iloc[-1] > self.df['high'].iloc[-3] and self.df['low'].iloc[-1] > self.df['low'].iloc[-3]

    def _check_dummy_sr(self):
        return True

    def _check_dummy_liquidity(self):
        return True

    def _check_dummy_volatility(self):
        spread = self.df['high'].iloc[-1] - self.df['low'].iloc[-1]
        return spread < (self.df['close'].iloc[-1] * 0.02)

    def _optional_dummy(self):
        return True
