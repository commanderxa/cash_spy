from sqlalchemy.orm import Session

from ..models import card as m_card
from ..schemes import card as s_card


def get_cards_by_user_id(db: Session, user_id: int):
    return db.query(m_card.Card).filter(m_card.UserCard.user_id == user_id).all()


def add_card(db: Session, card: s_card.Card):
    db_card = m_card.Card(user_id=card.user_id, bank_id=card.bank_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
