from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
