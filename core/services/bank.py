from sqlalchemy.orm import Session

from ..models import bank as m_bank


def get_banks(db: Session):
    return db.query(m_bank.Bank).all()


def get_bank(db: Session, id: int):
    return db.query(m_bank.Bank).filter(m_bank.Bank.id == id).first()
