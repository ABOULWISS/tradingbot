
from ServerSide.DataLair.DatabaseManager.database import Base
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func


class Fibonacci(Base):
    __tablename__ = "fibonacci"

    FibonacciID = Column(Integer, primary_key=True, index=True)
    MarketStructureID = Column(Integer, ForeignKey("market_structure.MarketStructureID"), nullable=False)
    LiquidityID = Column(Integer, ForeignKey("liquidity.LiquidityID"), nullable=False)
    IsValid = Column(Boolean, default=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
