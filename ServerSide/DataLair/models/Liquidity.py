

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, Enum, String
from sqlalchemy.sql import func
from DataLair.DatabaseManager.database import Base
import enum


class LiquiditySideType(str, enum.Enum):
    bullish = "bullish"
    bearish = "bearish"


class LiquidityTypeEnum(str, enum.Enum):
    stop_hunt = "stop-hunt"
    supply = "supply"
    demand = "demand"
    liquidity_pool = "liquidity-pool"


class Liquidity(Base):
    __tablename__ = "liquidity"

    LiquidityID = Column(Integer, primary_key=True, index=True)
    
    MarketStructureID = Column(Integer, ForeignKey("market_structure.MarketStructureID"), nullable=False)
    MarketDataID = Column(Integer, ForeignKey("market_data.MarketDataID"), nullable=True)
    
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    
    LiquidityType = Column(Enum(LiquidityTypeEnum), nullable=False)
    ZoneHigh = Column(Float, nullable=False)
    ZoneLow = Column(Float, nullable=False)
    LiquiditySide = Column(Enum(LiquiditySideType), nullable=False)
    
    IsTaken = Column(Boolean, default=False)
    
  



