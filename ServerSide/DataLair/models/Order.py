

from DataLair.DatabaseManager.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Order(Base):
    __tablename__ = "orders"

    OrderID = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    PositionID = Column(Integer, ForeignKey("position.PositionID"), nullable=False)
    AccountID = Column(Integer, ForeignKey("account.AccountID"), nullable=False)

    OrderType = Column(String(50), nullable=False)     # e.g., BUY, SELL, SL, TP, CLOSE
    Status = Column(String(50), nullable=False)        # e.g., Pending, Filled, Canceled, Rejected

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    position = relationship("Position", backref="orders")
    account = relationship("Account", backref="orders")
