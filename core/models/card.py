from sqlalchemy import Column, ForeignKey, Integer, String
from core.database import Base


class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(ForeignKey("users.id"))
    card_id = Column(ForeignKey("cards.id"))


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bank_id = Column(ForeignKey("banks.id"))
