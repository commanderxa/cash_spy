from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bank_id = Column(ForeignKey("banks.id"))

    user_cards = relationship("UserCard", back_populates="card")
    bank = relationship("Bank")


class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    card_id = Column(ForeignKey("cards.id"))

    card = relationship("Card", back_populates="user_cards")
