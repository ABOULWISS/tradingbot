



from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from DataLair.DatabaseManager.database import Base
import enum


class DirectionType(str, enum.Enum):
    bullish = "bullish"
    bearish = "bearish"



class OrderBlock(Base):
    __tablename__ = "order_blocks"

    OrderBlockID = Column(Integer, primary_key=True, index=True)

    # Link to MarketStructure
    MarketStructureID = Column(Integer, ForeignKey("market_structure.MarketStructureID"), nullable=False)

    # Prices
    OpenAt = Column(Float, nullable=False)
    CloseAt = Column(Float, nullable=False)
    High = Column(Float, nullable=True)
    Low = Column(Float, nullable=True)

    # Direction
    Direction = Column(Enum(DirectionType), nullable=False)

    # Status flags
    IsBroken = Column(Boolean, default=False)
    BreakCandleID = Column(Integer, ForeignKey("market_data.MarketDataID"), nullable=True)
    IsMitigated = Column(Boolean, default=False)
    IsValid = Column(Boolean, default=True)

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())