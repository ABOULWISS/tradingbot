

import pandas as pd
#from DataLair.marketdata import data



class MarketStructure:

    def __init__(self, data, lookback=2):
        self.data = data
        self.lookback = lookback
        self.swing_highs = []
        self.swing_lows = []
        self.labels = []
        self.trend = None

    # ----------------------------------------------------
    # 1) FIND SWINGS
    # ----------------------------------------------------
    def find_swings(self):
        highs = self.data['high']
        lows = self.data['low']

        swing_highs = []
        swing_lows = []

        for i in range(self.lookback, len(self.data) - self.lookback):
            window_high = highs[i-self.lookback:i+self.lookback+1]
            window_low = lows[i-self.lookback:i+self.lookback+1]

            if highs[i] == max(window_high):
                swing_highs.append((i, highs[i]))

            if lows[i] == min(window_low):
                swing_lows.append((i, lows[i]))

        self.swing_highs = swing_highs
        self.swing_lows = swing_lows

        return swing_highs, swing_lows

    # ----------------------------------------------------
    # 2) LABEL HH, LH, HL, LL
    # ----------------------------------------------------
    def label_swings(self):

        labels = []

        for idx, price in self.swing_highs:
            labels.append({"type": "SH", "idx": idx, "price": price})

        for idx, price in self.swing_lows:
            labels.append({"type": "SL", "idx": idx, "price": price})

        labels = sorted(labels, key=lambda x: x["idx"])

        last_high = None
        last_low = None

        for item in labels:

            if item["type"] == "SH":   # Swing High
                if last_high is None:
                    item["structure"] = "SH"
                else:
                    if item["price"] > last_high:
                        item["structure"] = "HH"
                    else:
                        item["structure"] = "LH"
                last_high = item["price"]

            elif item["type"] == "SL":  # Swing Low
                if last_low is None:
                    item["structure"] = "SL"
                else:
                    if item["price"] > last_low:
                        item["structure"] = "HL"
                    else:
                        item["structure"] = "LL"
                last_low = item["price"]

        self.labels = labels
        return labels

    # ----------------------------------------------------
    # 3) GET TREND
    # ----------------------------------------------------
    def get_trend(self):

        higher_highs = 0
        lower_lows = 0

        for l in self.labels:
            if l["structure"] == "HH":
                higher_highs += 1
            if l["structure"] == "LL":
                lower_lows += 1

        if higher_highs > lower_lows:
            self.trend = "BULLISH"
        elif lower_lows > higher_highs:
            self.trend = "BEARISH"
        else:
            self.trend = "SIDEWAYS"

        return self.trend

    # ----------------------------------------------------
    # 4) MAIN PIPELINE
    # ----------------------------------------------------
    def run(self):
        self.find_swings()
        self.label_swings()
        self.get_trend()
        return self.labels, self.trend