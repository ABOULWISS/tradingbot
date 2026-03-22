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

        if not labels:
            return 0

        df = self._labels_to_dataframe(labels)
        self.collector.store_market_structure(df)

        return len(labels)


         











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
                "bos": l["structure"] in ["HH", "LL"],
                "choch": l["structure"] in ["HL", "LH"],
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







   
    def label_swings(self):
        labels = []

        for idx, price in self.swing_highs:
            labels.append({"type": "SH", "idx": idx, "price": price})

        for idx, price in self.swing_lows:
            labels.append({"type": "SL", "idx": idx, "price": price})

        labels.sort(key=lambda x: x["idx"])

        last_high = None
        last_low = None

        for item in labels:
            if item["type"] == "SH":
                item["structure"] = "HH" if last_high and item["price"] > last_high else "LH"
                last_high = item["price"]
            else:
                item["structure"] = "HL" if last_low and item["price"] > last_low else "LL"
                last_low = item["price"]

        self.labels = labels
        return labels
    

    # ----------------------------------------------------
    # GET TREND
    # ----------------------------------------------------
    def get_trend(self):
        hh = sum(1 for l in self.labels if l["structure"] == "HH")
        ll = sum(1 for l in self.labels if l["structure"] == "LL")

        if hh > ll:
            self.trend = "BULLISH"
        elif ll > hh:
            self.trend = "BEARISH"
        else:
            self.trend = "SIDEWAYS"

        return self.trend
    

    def get_all_market_structure_data(self):
        df = self.collector.get_all_market_structure_and_market_data()
        return df
    
    def get_market_structure_per_timeframe(self, timeframe: str):
        df = self.collector.get_all_market_structure_per_timeframe(timeframe)
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

        if not labels:
            return pd.DataFrame()

        df = self._labels_to_dataframe(labels)
        self.collector.store_market_structure(df)

        return len(labels)





"""
    def _labels_to_dataframe(self, labels: List[Dict]) -> pd.DataFrame:
        rows = []

        for l in labels:
            market_data_id = int(self.data.iloc[l["idx"]]["MarketDataID"])
            timestamp = self.timestamp
    
    
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
                "bos": l["structure"] in ["HH", "LL"],
                "choch": l["structure"] in ["HL", "LH"],
            })

        return pd.DataFrame(rows)

        

    def store_market_structure_per_timeframe(self, timeframe: str):

        market_data = MarketDataEngine(symbol_id =1, timeframe="1m")
        data = market_data.get_all_candles_per_timeframe(timeframe)

        if data.empty:
            return pd.DataFrame()
        
        self.data = data
        self.timeframe = timeframe 
        self.find_swings()
        labels = self.label_swings()
        
        if not labels:
            return pd.DataFrame()
        
        df = self._labels_to_dataframe(labels)

        self.collector.store_market_structure(df)

        return len(labels)




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







   
    def label_swings(self):
        labels = []

        for idx, price in self.swing_highs:
            labels.append({"type": "SH", "idx": idx, "price": price})

        for idx, price in self.swing_lows:
            labels.append({"type": "SL", "idx": idx, "price": price})

        labels.sort(key=lambda x: x["idx"])

        last_high = None
        last_low = None

        for item in labels:
            if item["type"] == "SH":
                item["structure"] = "HH" if last_high and item["price"] > last_high else "LH"
                last_high = item["price"]
            else:
                item["structure"] = "HL" if last_low and item["price"] > last_low else "LL"
                last_low = item["price"]

        self.labels = labels
        return labels
    
"""












"""

    def _labels_to_dataframe(self, labels: List[Dict]) -> pd.DataFrame:
        rows = []

        for l in labels:

            row = self.data.iloc[l["idx"]]   # ✅ separate variable
            market_data_id = int(row["MarketDataID"])

            rows.append({
                "market_data_id": market_data_id,
                "timestamp": l["Timestamp"],
                "structure_type": StructureType(l["structure"]),
                "direction": (
                    DirectionType.bullish
                    if l["structure"] in ["HH", "HL"]
                    else DirectionType.bearish
                ),
                "timeframe": self.timeframe,
                "bos": l["structure"] in ["HH", "LL"],
                "choch": l["structure"] in ["HL", "LH"],
            })

        return pd.DataFrame(rows)

    # ----------------------------------------------------
    # FIND SWINGS
    # ----------------------------------------------------
    def find_swings(self):
        highs = self.data["High"]
        lows = self.data["Low"]
        timestamps = self.data["Timestamp"]

        swing_highs = []
        swing_lows = []



        for i in range(self.lookback, len(self.data) - self.lookback):



            if highs.iloc[i] == max(highs.iloc[i-self.lookback:i+self.lookback+1]):
                swing_highs.append({
                    "index": i,
                    "price": highs.iloc[i],
                    "timestamp": timestamps.iloc[i]
                })



            if lows.iloc[i] == min(lows.iloc[i-self.lookback:i+self.lookback+1]):
                swing_lows.append({
                    "index": i,
                    "price": lows.iloc[i],
                    "timestamp": timestamps.iloc[i]
                })



        self.swing_highs = swing_highs
        self.swing_lows = swing_lows





    def label_swings(self):
        labels = []

        # Convert swing highs
        for swing in self.swing_highs:
            labels.append({
                "type": "SH",
                "idx": swing["index"],
                "price": swing["price"],
                "timestamp": swing["timestamp"]
            })

        # Convert swing lows
        for swing in self.swing_lows:
            labels.append({
                "type": "SL",
                "idx": swing["index"],
                "price": swing["price"],
                "timestamp": swing["timestamp"]
            })

        # Sort by candle index
        labels.sort(key=lambda x: x["idx"])

        last_high = None
        last_low = None

        for item in labels:
            if item["type"] == "SH":
                item["structure"] = "HH" if last_high and item["price"] > last_high else "LH"
                last_high = item["price"]
            else:
                item["structure"] = "HL" if last_low and item["price"] > last_low else "LL"
                last_low = item["price"]

        self.labels = labels
        return labels

 
"""