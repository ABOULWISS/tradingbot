import pandas as pd
from typing import List, Dict
from DataLair.MarketStructureData import MarketStructureCollector
from CoreEngineLair.MarketDataEngine import MarketDataEngine
from DataLair.models.MarketStructure import StructureType, DirectionType


class MarketStructureService:
    """
    Business layer for Market Structure logic
    """

    def __init__(self, lookback: int = 2):
        self.collector = MarketStructureCollector()
        self.lookback = lookback

        self.data = None
        self.swing_highs = []
        self.swing_lows = []
        self.labels = []
        self.trend = None
        self.timeframe = None
        self.timestamp = None 

 

    

    def load_data(self):
        market_data = MarketDataEngine(symbol_id=1, timeframe="1m")

        
        data = pd.DataFrame(market_data.get_all_market_data_dfL())

        # 🔥 Ensure DataFrame
        if isinstance(data, list):
            self.data = pd.DataFrame(data)
        else:
            self.data = data




    def process_and_store_structure(self) -> int:
        self.load_data()
        self.find_swings()
        labels = self.label_swings()
        l = self.detect_choch()

        if not labels:
           return 0
    
        df = self._labels_to_dataframe(l)
        self.collector.store_market_structure(df)

        return len(l)


         




    def _labels_to_dataframe(self, labels: List[Dict]) -> pd.DataFrame:
        rows = []

        for l in labels:
          
            row = self.data.iloc[l["idx"]]

            market_data_id = int(row["MarketDataID"])
            timestamp = int(row["Timestamp"])
    
    
            rows.append({
                "market_data_id": market_data_id,
                "timestamp": timestamp,
                "structure_type": StructureType(l["structure"]),
                "direction": (
                    DirectionType.bullish
                    if l["structure"] in ["HH", "HL"]
                    else DirectionType.bearish
                ),
                "timeframe": self.timeframe,
                "bos": l["bos"],
                "choch": l["choch"],
            })

        return pd.DataFrame(rows)

        






    def find_swings(self):
        highs = self.data["High"]
        lows = self.data["Low"]
        swing_highs = []
        swing_lows = []

        for i in range(self.lookback, len(self.data) - self.lookback):

            if highs.iloc[i] == highs.iloc[i-self.lookback:i+self.lookback+1].max():
                swing_highs.append((i, highs.iloc[i]))

            if lows.iloc[i] == lows.iloc[i-self.lookback:i+self.lookback+1].min():
                swing_lows.append((i, lows.iloc[i]))

        self.swing_highs = swing_highs
        self.swing_lows = swing_lows





    def detect_bos(self, labels):
        result = []

        trend = None
        last_hh_index = None
        last_ll_index = None

        last_hh_price = None
        last_ll_price = None

        for i, l in enumerate(labels):
            structure = l["structure"]
            price = l["price"]

            result.append({
                **l,
                "bos": False
            })

            # -------------------------
            # DETECT BOS
            # -------------------------
            if trend == "bullish":
                if structure == "HH" and last_hh_price is not None:
                    if price > last_hh_price:
                        result[i]["bos"] = True  # mark current HH

            elif trend == "bearish":
                if structure == "LL" and last_ll_price is not None:
                    if price < last_ll_price:
                        result[i]["bos"] = True  # mark current LL

            # -------------------------
            # UPDATE LEVELS
            # -------------------------
            if structure == "HH":
                last_hh_index = i
                last_hh_price = price

            elif structure == "LL":
                last_ll_index = i
                last_ll_price = price

            # -------------------------
            # UPDATE TREND
            # -------------------------
            if structure in ["HH", "HL"]:
                trend = "bullish"
            elif structure in ["LL", "LH"]:
                trend = "bearish"

        return result


   
    def detect_choch(self, labels):
        result = []

        trend = None
        last_hh_index = None
        last_hl_index = None
        last_lh_index = None
        last_ll_index = None

        for i, l in enumerate(labels):
            structure = l["structure"]

            result.append({
                **l,
                "choch": False,
                
            })

            # -------------------------
            # DETECT CHOCH FIRST (IMPORTANT)
            # -------------------------
            if trend == "bullish":
                # shift to bearish → HL broken
                if structure in ["LL", "LH"]:
                    if last_hl_index is not None:
                        result[last_hl_index]["choch"] = True
                    trend = "bearish"

            elif trend == "bearish":
                # shift to bullish → LH broken
                if structure in ["HH", "HL"]:
                    if last_lh_index is not None:
                        result[last_lh_index]["choch"] = True
                    trend = "bullish"

            # -------------------------
            # UPDATE STRUCTURE LEVELS
            # -------------------------
            if structure == "HH":
                last_hh_index = i

            elif structure == "HL":
                last_hl_index = i

            elif structure == "LH":
                last_lh_index = i

            elif structure == "LL":
                last_ll_index = i

            # -------------------------
            # UPDATE TREND AFTER
            # -------------------------
            if structure in ["HH", "HL"]:
                trend = "bullish"
            elif structure in ["LL", "LH"]:
                trend = "bearish"

        return result





    def get_all_market_structure_data(self):
        df = self.collector.get_all_market_structure_and_market_data()
        return df
    
    def get_market_structure_per_timeframe(self, timeframe: str):
        df = self.collector.get_all_market_structure_per_timeframe(timeframe)
        return df
    
    def get_all_choch(self):
        df = self.collector.get_all_choch()
        return df
    
    def get_all_bos(self):
        df = self.collector.get_all_bos()
        return df



    def store_market_structure_per_timeframe(self, timeframe: str):

        market_data = MarketDataEngine(symbol_id=1, timeframe=timeframe)
        data =  pd.DataFrame(market_data.get_all_candles_per_timeframe(timeframe))

        if data.empty:
            return pd.DataFrame()

        self.data = data
        self.timeframe = timeframe

        self.find_swings()
        labels = self.label_swings()
        newlabels = self.detect_choch(labels)
        newlabels = self.detect_bos(newlabels)

        if labels is None or len(newlabels) == 0:
           return 0

        df = self._labels_to_dataframe(newlabels)
        self.collector.store_market_structure(df)

        return len(newlabels)






    def label_swings(self):
        labels = []

        # merge highs + lows and sort by index (time)
        points = []

        for idx, price in self.swing_highs:
            points.append({"idx": idx, "price": price, "type": "high"})

        for idx, price in self.swing_lows:
            points.append({"idx": idx, "price": price, "type": "low"})

        # sort by time
        points = sorted(points, key=lambda x: x["idx"])

        last_high = None
        last_low = None

        for p in points:
            idx = p["idx"]
            price = p["price"]

            structure = None

            if p["type"] == "high":
                if last_high is None:
                    structure = "HH"  # first one (can adjust later)
                else:
                    if price > last_high:
                        structure = "HH"
                    else:
                        structure = "LH"

                last_high = price

            elif p["type"] == "low":
                if last_low is None:
                    structure = "HL"  # first one (can adjust later)
                else:
                    if price > last_low:
                        structure = "HL"
                    else:
                        structure = "LL"

                last_low = price

            labels.append({
                "idx": idx,
                "price": price,
                "structure": structure
            })


        self.labels = labels
        return labels