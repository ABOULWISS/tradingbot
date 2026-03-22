





from DataLair.DatabaseManager.database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Position(Base):
    __tablename__ = "position"

    PositionID = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    AccountID = Column(Integer, ForeignKey("account.AccountID"), nullable=False)
    SymbolID = Column(Integer, ForeignKey("symbol.SymbolID"), nullable=False)
    StrategyID = Column(Integer, ForeignKey("strategy.StrategyID"), nullable=True)

    Direction = Column(String(10), nullable=False)    # BUY or SELL
    EntryPrice = Column(Float, nullable=False)
    StopLoss = Column(Float, nullable=True)
    TakeProfit = Column(Float, nullable=True)

    Size = Column(Float, nullable=False)              # lot size
    Status = Column(String(50), nullable=False)       # Open, Closed, Stopped, TP Hit, SL Hit, etc.

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    account = relationship("Account", backref="positions")
    symbol = relationship("Symbol", backref="positions")
    strategy = relationship("Strategy", backref="positions")