

from DataLair.DatabaseManager.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func


class Person(Base):
    __tablename__ = "person"

    PersonID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Phone = Column(String(50), unique=True, nullable=True)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())



