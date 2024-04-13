from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from ..database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=True)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)

    description = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    cashback = Column(Float)
    favorite_cashback = Column(Float, nullable=True)

    date_from = Column(DateTime, nullable=True)
    date_to = Column(DateTime, nullable=True)

    category = relationship("Category", back_populates="offers")
