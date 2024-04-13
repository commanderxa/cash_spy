from sqlalchemy.orm import Session

from ..models import bank as m_bank
from ..schemes import bank as s_bank


def get_banks(db: Session):
    return db.query(m_bank.Bank).all()


# def add_card(db: Session, card: s_card.Card):
#     db_card = m_card.Card(user_id=card.user_id, bank_id=card.bank_id)
#     db.add(db_card)
#     db.commit()
#     db.refresh(db_card)
#     return db_card
