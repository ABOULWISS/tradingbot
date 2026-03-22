


from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from DataLair.DatabaseManager.database import Base


class Strategy(Base):
    __tablename__ = "strategy"

    StrategyID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(50), nullable=False, unique=True)
    Description = Column(String(200), nullable=True)
    IsActive = Column(Boolean, default=True)

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())
