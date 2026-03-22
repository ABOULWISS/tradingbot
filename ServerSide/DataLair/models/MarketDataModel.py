






from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.sql import func
from DataLair.DatabaseManager.database import Base 
from sqlalchemy.orm import relationship


class MarketData(Base):
    __tablename__ = "market_data"

    MarketDataID = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    SymbolID = Column(Integer, ForeignKey("symbol.SymbolID"), nullable=False)
    symbol = relationship("Symbol", backref="market_data")

    # Candle timestamp (open time of the candle)
    Timestamp = Column(DateTime(timezone=True), nullable=False)

    # OHLCV
    Open = Column(Float, nullable=False)
    High = Column(Float, nullable=False)
    Low = Column(Float, nullable=False)
    Close = Column(Float, nullable=False)
    TimeFrame = Column(String(10), nullable=False)
    Volume = Column(Float)

    Source = Column(String)  # MT5, Binance, etc.

    CollectedAt = Column(DateTime(timezone=True), server_default=func.now())

    

    market_structures = relationship(
        "MarketStructure",
        back_populates="market_data",
        cascade="all, delete-orphan"
    )





    __table_args__ = (
        UniqueConstraint(
            "SymbolID",
            "Timestamp",
            name="uix_symbol_timestamp"
        ),
    )
