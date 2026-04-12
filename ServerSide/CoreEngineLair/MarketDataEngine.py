
from DataLair.MarketData import MarketDataCollector
from DataLair.models.MarketDataModel import MarketData
import asyncio, time, random
import pandas as pd

class MarketDataEngine:



    def __init__(self, symbol_id: int, timeframe: str):


        self.collector = MarketDataCollector()  # no API keys needed
        self.symbol_id = symbol_id       
        self.timeframe = timeframe 
        self.current_candle = None 
        self.MarketDataID = 0
        self.SymbolID = 0
        self.Open = 0
        self.High = 0
        self.Low = 0
        self.Close = 0
        self.TimeFrame = ""
        self.Volume = 0
        self.Source = ""  



    # Collect only
    def collect_market_data(self, symbol: str, timeframe: str, start: str = "1 day ago UTC"):
        df = self.collector.fetch_historical_klines(symbol, timeframe, start)
        return df

    # Store only
    def store_market_data(self, symbol: str, timeframe: str, start: str = "1 day ago UTC"):
        df = self.collector.fetch_historical_klines(symbol, timeframe, start)
        self.collector.store_market_data(df)
        return {"status": "success", "rows": len(df)}
    

    # Get All MarketData
    def get_all_market_dataL(self):
        df = self.collector.get_all_market_data()
        return df
    

        # Get All MarketData
    def get_all_market_data_dfL(self):
        df = self.collector.get_all_market_data_df()
        return df
    
    def get_market_data_by_id(self, data_id: int):
        df = self.collector.get_market_data_by_id_df(data_id)
        # convert DataFrame to JSON-serializable format
        return df.to_dict(orient="records")


   
        
        


    def get_all_candles_per_timeframe(self, timeframe : str):
       # self.collector.delete_old_all()
        df = self.collector.get_all_market_data_df()

        # Defensive checks
        if df.empty:
            return []

        #df.columns = df.columns.str.lower()
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
        df = df.set_index("Timestamp").sort_index()

        # 🔥 Timeframe mapping (IMPORTANT)
        timeframe_map = {
            "1m": "1T",
            "5m": "5T",
            "15m": "15T",
            "1h": "1h",
            "4h": "4h",
            "1d": "1D",
        }

        if timeframe not in timeframe_map:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        rule = timeframe_map[timeframe]

        df_tf = (
            df.resample(rule, label="right", closed="right")
            .agg({
                "MarketDataID": "first",
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            })
            .dropna()
            .reset_index()
        )

        # Convert timestamp → unix seconds
        df_tf["Timestamp"] = (df_tf["Timestamp"].astype("int64") // 10**9)

        return df_tf.to_dict(orient="records")



    def get_all_marketstructures_per_timeframe(self, timeframe: str) -> pd.DataFrame:
        # 1️⃣ Get raw data
        df = self.collector.get_all_market_data_df()

        if df.empty:
            return pd.DataFrame()
        
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
        df = df.set_index("Timestamp").sort_index()
     

        # 3️⃣ Timeframe mapping
        timeframe_map = {
            "1m": "1T",
            "5m": "5T",
            "15m": "15T",
            "1H": "1H",
            "4H": "4H",
            "1d": "1D",
        }

        if timeframe not in timeframe_map:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        rule = timeframe_map[timeframe]

        # 4️⃣ Resample / aggregate
        df_tf = (
            df.resample(rule, label="right", closed="right")
            .agg({
                "MarketDataID": "first",
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            })
            .dropna()
            .reset_index()
        )

        # Convert timestamp → unix seconds
        df_tf["Timestamp"] = (df_tf["Timestamp"].astype("int64") // 10**9)
        
        return df_tf




    def floor_minute(self,ts):
        return ts - (ts % 60)



    def new_candle(self,price, ts):


        return {

            "time": self.floor_minute(ts),
            "open": price,
            "high": price,
            "low": price,
            "close": price

        }



    def update_candle(self,candle, price):
        candle["high"] = max(candle["high"], price)
        candle["low"] = min(candle["low"], price)
        candle["close"] = price
    




    def process_tick(self, price, ts):

        if self.current_candle is None:
            self.current_candle = self.new_candle(price, ts)
            return self.current_candle

        if self.floor_minute(ts) != self.current_candle["time"]:
            self.collector.save_candle(
                candle=self.current_candle,
                symbol_id=self.symbol_id,
                timeframe=self.timeframe,
            )
            self.current_candle = self.new_candle(price, ts)
        else:
            self.update_candle(self.current_candle, price)

        return self.current_candle
    







    async def price_feed(self):
        import random, time
        price = 86000.0

        while True:
            await asyncio.sleep(1)
            price += random.uniform(-10, 10)
            ts = int(time.time())

            # process candle
            candle = self.process_tick(price, ts)

            # return candle for broadcasting (API layer handles WebSocket)
            yield candle

        


    






























