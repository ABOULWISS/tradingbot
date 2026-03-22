




from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from DataLair.DatabaseManager.database import Base


class Symbol(Base):
    __tablename__ = "symbol"

    SymbolID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    Name = Column(String(20), nullable=False, unique=True)   # e.g., 'EURUSD', 'XAUUSD'
