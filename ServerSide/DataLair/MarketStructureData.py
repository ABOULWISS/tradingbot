







from pytz import timezone
from sqlalchemy.orm import Session
from DataLair.models.MarketStructure import MarketStructure, StructureType, DirectionType
from DataLair.DatabaseManager.database import SessionLocal
from DataLair.models.MarketDataModel import MarketData
from typing import List, Tuple
from sqlalchemy import select
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert


class MarketStructureCollector:

    def __init__(self):
        pass




    def ms_to_datetime(self , ms: int):
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    # ----------------------------------------------------
    # Store Market Structure
    # ----------------------------------------------------
    def store_market_structureee(self, df: pd.DataFrame ):

        if df.empty:
            return

        session: Session = SessionLocal()

        try:
            for _, row in df.iterrows():

                ms = MarketStructure(
                    MarketDataID=int(row["market_data_id"]),

                    Type=StructureType(row["structure_type"]),  
                    Direction=DirectionType(row["direction"]) if row["direction"] else None,
                    BOS=bool(row.get("bos", False)),
                    CHOCH=bool(row.get("choch", False)),
                    TimeFrame = row["timeframe"],
                    Timestamp= self.ms_to_datetime(row["timestamp"]),
                )

                session.add(ms)

            session.commit()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()







    def store_market_structure(self, df: pd.DataFrame):

        # 🔒 Safety: do nothing if no data
        if df.empty:
            return

        session: Session = SessionLocal()

        try:
            records = []

            # 🔁 Prepare bulk records
            for _, row in df.iterrows():
                records.append({
                    "MarketDataID": int(row["market_data_id"]),
                    "Type": StructureType(row["structure_type"]),
                    "Direction": DirectionType(row["direction"]) if row["direction"] else None,
                    "BOS": bool(row.get("bos", False)),
                    "CHOCH": bool(row.get("choch", False)),
                    "TimeFrame": row["timeframe"],
                    "Timestamp": self.ms_to_datetime(row["timestamp"]),
                })

            # 🚀 Bulk insert
            stmt = insert(MarketStructure).values(records)



            # 🛑 Prevent duplicates (matches UNIQUE constraint)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=["MarketDataID", "Timestamp"]
            )



            session.execute(stmt)
            session.commit()



        except Exception as e:
            session.rollback()
            raise e



        finally:
            session.close()







    # ----------------------------------------------------
    # Fetch Market Structure (chart / analysis ready)
    # ----------------------------------------------------
    def get_all_market_structure(self):
        session: Session = SessionLocal()

        try:
            structures = (
                session.query(MarketStructure)
                .order_by(MarketStructure.CreatedAt.asc())
                .all()
            )

            result = []
            for s in structures:
                result.append({
                    "id": s.MarketStructureID,
                    "market_data_id": s.MarketDataID,
                    "type": s.Type.value,
                    "direction": s.Direction.value if s.Direction else None,
                    "bos": s.BOS,
                    "choch": s.CHOCH,
                    "created_at": int(s.CreatedAt.timestamp()),
                })

            return result

        finally:
            session.close()




    def get_all_choch(self):
        session: Session = SessionLocal()

        try:
            structures = (
                session.query(MarketStructure)
                .filter(MarketStructure.CHOCH == True)   
                .order_by(MarketStructure.CreatedAt.asc())
                .all()
            )

            result = []
            for s in structures:
                result.append({
                    "id": s.MarketStructureID,
                    "market_data_id": s.MarketDataID,
                    "type": s.Type.value,
                    "direction": s.Direction.value if s.Direction else None,
                    "bos": s.BOS,
                    "choch": s.CHOCH,
                    "created_at": int(s.CreatedAt.timestamp()),
                })

            return result



        finally:
            session.close()
    

    def get_all_bos(self):
        session: Session = SessionLocal()

        try:
            structures = (
                session.query(MarketStructure)
                .filter(MarketStructure.BOS == True)   
                .order_by(MarketStructure.CreatedAt.asc())
                .all()
            )

            result = []
            for s in structures:
                result.append({
                    "id": s.MarketStructureID,
                    "market_data_id": s.MarketDataID,
                    "type": s.Type.value,
                    "direction": s.Direction.value if s.Direction else None,
                    "bos": s.BOS,
                    "choch": s.CHOCH,
                    "created_at": int(s.CreatedAt.timestamp()),
                })

            return result



        finally:
            session.close()
  

    def get_all_market_structure_and_market_data(self):


        session: Session = SessionLocal()

        try:

            data: List[Tuple[MarketStructure, MarketData]] = (
                session.query(MarketStructure, MarketData)
                .join(MarketStructure.market_data)
                .all()
            )



 
            result = []
            for structure, market_data in data:
                result.append({
                    
                    "id": structure.MarketStructureID,
                    "market_data_id": structure.MarketDataID,
                    "type": structure.Type.value,
                    "direction": structure.Direction.value if structure.Direction else None,
                    "bos": structure.BOS,
                    "choch": structure.CHOCH,
                    "created_at": int(structure.CreatedAt.timestamp()),



                    # 🔥 بيانات الشمعة مباشرة
                    "time": int(market_data.Timestamp.timestamp()),
                    "open": market_data.Open,
                    "high": market_data.High,
                    "low": market_data.Low,
                    "close": market_data.Close,
                 
                })

                

            return result



        finally:
            session.close()











    def get_all_market_structure_per_timeframe(self, timeframe: str):

        session: Session = SessionLocal()

        try:
            data: List[Tuple[MarketStructure, MarketData]] = (
                        session.query(MarketStructure, MarketData)
                        .join(MarketStructure.market_data)
                        .filter(MarketStructure.TimeFrame == timeframe)
                        .all()
           )



            result = []

            for structure, market_data in data:
                result.append({
                    "id": structure.MarketStructureID,
                    "market_data_id": structure.MarketDataID,
                    "type": structure.Type.value,
                    "direction": structure.Direction.value if structure.Direction else None,
                    "bos": structure.BOS,
                    "choch": structure.CHOCH,
                    "created_at": int(structure.CreatedAt.timestamp()),
                    "time_stamp": int(market_data.Timestamp.timestamp()),
                   
                    "open": market_data.Open,
                    "high": market_data.High,
                    "low": market_data.Low,
                    "close": market_data.Close,
                })

            return result

        finally:
            session.close()



