from sqlalchemy.orm import Session

from ..models import card as m_card
from ..models import bank as m_bank
from ..models import partner as m_partner
from ..models import category as m_category
from ..models import offer as m_offer
from ..schemes import offer as s_offer


def get_offers_by_place(db: Session, place: str):
    return (
        db.query(m_offer.Offer)
        .filter(m_offer.Offer.partner.ilike(f"%{place}%"))
        .order_by(m_offer.Offer.cashback.desc())
        .all()
    )


def get_offers_by_category(db: Session, category: str, user_id: int):
    _category = (
        db.query(m_category.Category)
        .filter(m_category.Category.name.ilike(f"%{category}%"))
        .first()
    )
    offers = (
        db.query(m_offer.Offer)
        .join(
            m_card.Card, m_offer.Offer.card_id == m_card.Card.id
        )  # Join offers to cards
        .join(
            m_card.UserCard, m_card.UserCard.card_id == m_card.Card.id
        )  # Join cards to user_cards
        .filter(m_card.UserCard.user_id == user_id)  # Filter for this specific user
        .filter(m_offer.Offer.category_id == _category.id)  # Filter by category
        .order_by(m_offer.Offer.cashback.desc())  # Order by cashback descending
        .all()
    )
    return offers


def get_offers_by_bank_cards(user_id: int, db: Session):
    offers = (
        db.query(m_offer.Offer)
        .join(
            m_card.Card, m_offer.Offer.card_id == m_card.Card.id
        )  # Join offers to cards
        .join(
            m_card.UserCard, m_card.UserCard.card_id == m_card.Card.id
        )  # Join cards to user_cards
        .filter(m_card.UserCard.user_id == user_id)  # Filter for this specific user
        .filter(m_offer.Offer.category_id == None)  # Filter by category
        .filter(m_offer.Offer.partner == None)  # Filter by category
        .order_by(m_offer.Offer.cashback.desc())  # Order by cashback descending
        .all()
    )
    return offers


def add_offer(db: Session, offer: s_offer.OfferCreate):
    db_offer = m_offer.Offer(
        name=offer.name,
        category_id=offer.category_id,
        card_id=offer.card_id,
        partner=offer.partner,
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
