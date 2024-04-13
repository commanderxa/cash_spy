from sqlalchemy.orm import Session

from ..models import offer as m_offer
from ..schemes import offer as s_offer


# def get_user(db: Session, user_id: int):
#     return db.query(m_user.User).filter(m_user.User.id == user_id).first()


# def get_offers_by_user(db: Session, username: str):
#     return db.query(m_user.User).filter(m_user.User.username == username).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(m_user.User).offset(skip).limit(limit).all()


def add_offer(db: Session, offer: s_offer.OfferCreate):
    db_offer = m_offer.Offer(
        name=offer.name,
        category_id=offer.category_id,
        card_id=offer.card_id,
        partner_id=offer.partner_id,
        description=offer.description,
        condition=offer.condition,
        cashback=offer.cashback,
        favorite_cashback=offer.favorite_cashback,
        date_from=offer.date_from,
        date_to=offer.date_to,
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer
