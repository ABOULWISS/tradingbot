


from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum , BigInteger
from sqlalchemy.sql import func
from DataLair.DatabaseManager.database import Base
import enum
from sqlalchemy.orm import relationship

# Optional: Enum for structure type
class StructureType(str, enum.Enum):
    HH = "HH"
    HL = "HL"
    LH = "LH"
    LL = "LL"


# Optional: Enum for direction
class DirectionType(str, enum.Enum):
    bullish = "bullish"
    bearish = "bearish"


class MarketStructure(Base):
    __tablename__ = "market_structure"

    MarketStructureID = Column(Integer, primary_key=True, index=True)
    
    # FK to the candle that created the structure signal
    MarketDataID = Column(Integer, ForeignKey("market_data.MarketDataID"), nullable=False)
    
    # HH | HL | LH | LL
    Type = Column(Enum(StructureType), nullable=False)
    
    # bullish | bearish
    Direction = Column(Enum(DirectionType), nullable=True)
    
    # BOS and CHOCH flags
    BOS = Column(Boolean, default=False)     # Break of Structure
    
    CHOCH = Column(Boolean, default=False)   # Change of Character
    
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    
    TimeFrame = Column(String(10), nullable=False)
    
    Timestamp = Column(DateTime(timezone=True), nullable=False)


    market_data = relationship(
        "MarketData",
        back_populates="market_structures"
    )





