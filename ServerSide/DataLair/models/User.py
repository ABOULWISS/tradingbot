





from DataLair.DatabaseManager.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    UserID = Column(Integer, primary_key=True, index=True)

    # FK → Person table
    PersonID = Column(Integer, ForeignKey("person.PersonID"), nullable=False)

    Username = Column(String(100), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    IsAdmin = Column(Boolean, default=False)
    IsActive = Column(Boolean, default=True)

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to Person
    person = relationship("Person", backref="user")