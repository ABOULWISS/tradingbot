from binance.client import Client
from sqlalchemy.orm import Session
from DataLair.models.MarketDataModel import MarketData 
from DataLair.DatabaseManager.database import SessionLocal
from DataLair.models.Symbol import Symbol
import pandas as pd
from datetime import datetime, timezone





class MarketDataCollector:

    def __init__(self):
        self.client = Client() 
        
        
        
      
    
    # ----------------------------------------------------
    # Fetch historical klines
    # ----------------------------------------------------
    def fetch_historical_klines(
        self,
        symbol: str,
        interval: str,
        start: str = "1 day ago UTC"
    ) -> pd.DataFrame:

        try:
            klines = self.client.get_historical_klines(symbol, interval, start)
        except Exception as e:
            print(f"❌ Error fetching {symbol} {interval}: {e}")
            return pd.DataFrame()

        data = []
        for k in klines:
            data.append({
                "symbol": symbol,
                "timeframe": interval,
                "timestamp": int(k[0]),  # milliseconds
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
            })

        return pd.DataFrame(data)
    



     
    def ms_to_datetime(self , ms: int):
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    
    # ----------------------------------------------------
    # Store market data (FK ONLY)
    # ----------------------------------------------------
    def store_market_data(self, df: pd.DataFrame):

        if df.empty:
            return

        session: Session = SessionLocal()
        
        try:
            # ✅ Fetch symbol ONCE
            symbol_name = df.iloc[0]["symbol"]
            symbol = session.query(Symbol).filter_by(Name=symbol_name).first()
            
            
            if not symbol:
                raise ValueError(f"Symbol '{symbol_name}' not found in database")

            for _, row in df.iterrows():

                candle = MarketData(

                    SymbolID=symbol.SymbolID, 
                    Timestamp= self.ms_to_datetime(row["timestamp"]),
                    TimeFrame=row["timeframe"],
                    Open=row["open"],
                    High=row["high"],
                    Low=row["low"],
                    Close=row["close"],
                    Volume=row["volume"],
                    Source="Binance"

                )

                session.merge(candle)

            session.commit()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()
    

    def get_all_market_data(self):
        """
        Fetch all candles and return chart-ready data
        (lightweight-charts compatible)
        """
        session: Session = SessionLocal()

        try:
              candles_db = (
                  session.query(MarketData)
                  .order_by(MarketData.Timestamp.asc())
                  .all()
              )

              candles = []
              for candle in candles_db:
                  candles.append({
                      "MarketDataID" : candle.MarketDataID,
                      "time": int(candle.Timestamp.timestamp()),  # ✅ UNIX seconds
                      "open": candle.Open,
                      "high": candle.High,
                      "low": candle.Low,
                      "close": candle.Close,
                  })

              return candles  # ✅ LIST, NOT DataFrame

        finally:
              session.close()


    def get_all_market_data_df(self) -> pd.DataFrame:
        session: Session = SessionLocal()

        try:
            query = (
                session.query(
                    MarketData.MarketDataID,
                    MarketData.Timestamp,
                    MarketData.Open,
                    MarketData.High,
                    MarketData.Low,
                    MarketData.Close,
                    MarketData.Volume,
                    MarketData.TimeFrame,
                )
                .order_by(MarketData.Timestamp.asc())
            )

            df = pd.read_sql(query.statement, session.bind)
            return df

        finally:
            session.close()


    def get_market_data_by_id_df(self, data_id: int):
        session: Session = SessionLocal()

        try:
            query = (
                session.query(
                    MarketData.MarketDataID,   # ✅ COLUMN
                    MarketData.Timestamp,
                    MarketData.Open,
                    MarketData.High,
                    MarketData.Low,
                    MarketData.Close,
                    MarketData.Volume,
                    MarketData.TimeFrame,
                )
                .filter(MarketData.MarketDataID == data_id)
            )

            df = pd.read_sql(query.statement, session.bind)
            return df

        finally:
            session.close()








    def save_candle(
        self,
        candle: dict,
        symbol_id: int,
        timeframe: str,
       ):
        db = SessionLocal()
        try:
            ts = datetime.fromtimestamp(candle["time"], tz=timezone.utc)

            # prevent duplicate candle
            exists = (
                db.query(MarketData)
                .filter(
                    MarketData.SymbolID == symbol_id,
                    MarketData.TimeFrame == timeframe,
                    MarketData.Timestamp == ts,
                )
                .first()
            )

            if exists:
                return

            db.add(
                MarketData(
                    SymbolID=symbol_id,
                    Timestamp=ts,
                    TimeFrame=timeframe,
                    Open=candle["open"],
                    High=candle["high"],
                    Low=candle["low"],
                    Close=candle["close"],
                    Volume=0.0,
                    Source="LiveFeed",
                )
            )

            db.commit()

        finally:
            db.close()



