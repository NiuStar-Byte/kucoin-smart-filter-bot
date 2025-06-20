import numpy as np

class SmartFilter:
    def __init__(self, symbol, df, tf=None, min_score=12, required_passed=7):
        self.symbol = symbol
        self.df = df
        self.tf = tf
        self.min_score = min_score
        self.required_passed = required_passed
        self.result = None
        self.stack_results = {}
        self.total_score = 0
        self.passed_required = 0

    def analyze(self):
        self.stack_results = {
            "Fractal Zone": self.check_fractal_zone(),
            "EMA Cloud": self.check_ema_cloud(),
            "MACD": self.check_macd(),
            "Momentum": self.check_momentum(),
            "HATS": self.check_hats(),
            "Volume Spike": self.check_volume_spike(),
            "VWAP Divergence": self.check_vwap_divergence(),
            "MTF Volume Agreement": self.check_mtf_volume(),
            "HH/LL Trend": self.check_trend(),
            "EMA Structure": self.check_ema_structure(),
            "Chop Zone": self.check_chop_zone(),
            "Candle Confirmation": self.check_candle_confirmation(),
            "Wick Dominance": self.check_wick(),
            "Absorption": self.check_absorption(),
            "Support/Resistance": self.check_sr(),
            "Smart Money Bias": self.check_smart_money(),
            "Liquidity Pool": self.check_liquidity(),
            "Spread Filter": self.check_spread_filter()
        }

        self.total_score = sum(1 for passed in self.stack_results.values() if passed)
        self.passed_required = sum(1 for i, passed in enumerate(self.stack_results.values()) if i < 12 and passed)

        if self.total_score >= self.min_score and self.passed_required >= self.required_passed:
            self.result = {
                "symbol": self.symbol,
                "signal_type": "LONG",
                "price": self.df['close'].iloc[-1],
                "tf": self.tf,
                "score": self.total_score,
                "passed": self.passed_required
            }
            return self.result
        else:
            return None

    # -------------- STACK METHODS --------------
    def check_fractal_zone(self):
        return True if self.df['close'].iloc[-1] > self.df['close'].mean() else False

    def check_ema_cloud(self):
        return True if self.df['close'].iloc[-1] > self.df['ema20'].iloc[-1] else False

    def check_macd(self):
        return True if self.df['macd'].iloc[-1] > self.df['signal'].iloc[-1] else False

    def check_momentum(self):
        return True if self.df['rsi'].iloc[-1] > 55 else False

    def check_hats(self):
        return True if self.df['close'].iloc[-1] > self.df['ema9'].iloc[-1] else False

    def check_volume_spike(self):
        return True if self.df['volume'].iloc[-1] > 1.5 * self.df['volume'].rolling(20).mean().iloc[-1] else False

    def check_vwap_divergence(self):
        return True if abs(self.df['close'].iloc[-1] - self.df['vwap'].iloc[-1]) / self.df['close'].iloc[-1] > 0.01 else False

    def check_mtf_volume(self):
        return True if self.df['volume'].iloc[-1] > self.df['volume'].mean() else False

    def check_trend(self):
        return True if self.df['close'].iloc[-1] > self.df['close'].iloc[-5] else False

    def check_ema_structure(self):
        return True if self.df['ema9'].iloc[-1] > self.df['ema21'].iloc[-1] else False

    def check_chop_zone(self):
        return True if np.std(self.df['close'].tail(10)) < np.std(self.df['close'].tail(30)) else False

    def check_candle_confirmation(self):
        return True if self.df['close'].iloc[-1] > self.df['open'].iloc[-1] else False

    def check_wick(self):
        return True if (self.df['high'].iloc[-1] - self.df['close'].iloc[-1]) < (self.df['close'].iloc[-1] - self.df['low'].iloc[-1]) else False

    def check_absorption(self):
        return True if self.df['buy_volume'].iloc[-1] > self.df['sell_volume'].iloc[-1] else False

    def check_sr(self):
        return True if self.df['close'].iloc[-1] > self.df['support'].iloc[-1] else False

    def check_smart_money(self):
        return True if self.df['big_trades'].iloc[-1] > 0 else False

    def check_liquidity(self):
        return True if self.df['liquidity_score'].iloc[-1] > 70 else False

    def check_spread_filter(self):
        return True if (self.df['ask'].iloc[-1] - self.df['bid'].iloc[-1]) / self.df['close'].iloc[-1] < 0.002 else False
