from sqlalchemy.orm import Session

from ..models import card as m_card
from ..schemes import card as s_card


def get_cards_by_bank(db: Session, bank_id: int):
    return db.query(m_card.Card).filter(m_card.Card.bank_id == bank_id).all()


def get_cards_by_user(db: Session, user_id: int):
    return db.query(m_card.UserCard).filter(m_card.UserCard.user_id == user_id).all()


def get_card(db: Session, id: int):
    return db.query(m_card.Card).filter(m_card.Card.id == id).first()


def add_card(db: Session, card_id: int, user_id: int):
    db_card = m_card.UserCard(user_id=user_id, card_id=card_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
