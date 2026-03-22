





from DataLair.DatabaseManager.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Account(Base):
    __tablename__ = "account"

    AccountID = Column(Integer, primary_key=True, index=True)

    # FK → User table
    UserID = Column(Integer, ForeignKey("user.UserID"), nullable=False)

    Server = Column(String(100), nullable=False)
    Platform = Column(String(50), nullable=False)    # e.g., MT4, MT5, cTrader
    Password = Column(String(255), nullable=False)   # store encrypted/hash, recommended
    LoginNumber = Column(String(100), unique=True, nullable=False)
    AccountType = Column(String(50), nullable=False) # Real, Demo, Investor, etc.
    
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to User
    user = relationship("User", backref="accounts")
