from sqlalchemy.orm import Session

from core.models.card import Card
from core.models.offer import Offer
from core.models.bank import Bank
from core.models.category import Category
from core.database import SessionLocal, engine
from . import bank, category, offer, user, card


def create_tables():
    user.Base.metadata.create_all(bind=engine)
    bank.Base.metadata.create_all(bind=engine)
    category.Base.metadata.create_all(bind=engine)
    card.Base.metadata.create_all(bind=engine)
    offer.Base.metadata.create_all(bind=engine)


def fill_tables():
    db = SessionLocal()
    fill_categories(db)
    fill_banks(db)
    fill_cards(db)
    fill_offers(db)


def fill_categories(db: Session):
    category_data = [
        Category(name="Игровые сервисы"),
        Category(name="Салоны красоты и косметики"),
        Category(name="Одежда и обувь"),
        Category(name="Мебель"),
        Category(name="Медицинские услуги"),
        Category(name="Кафе и рестораны"),
        Category(name="Такси"),
        Category(name="Онлайн кино и музыка"),
        Category(name="Путешествия"),
        Category(name="Фитнес и SPA"),
        Category(name="Супермаркеты"),
        Category(name="Образование"),
        Category(name="Доставка еды"),
        Category(name="Питомцы"),
        Category(name="Товары для детей"),
    ]

    for category in category_data:
        # Check if category already exists to avoid duplicates
        db_category = db.query(Category).filter(Category.name == category.name).first()
        if not db_category:
            db.add(category)

    db.commit()


def fill_banks(db: Session):
    bank_data = [
        Bank(name="Halyk Bank"),
        Bank(name="Jysan Bank"),
        Bank(name="Bank Center Credit"),
    ]

    for bank in bank_data:
        # Check if bank already exists to avoid duplicates
        db_bank = db.query(Bank).filter(Bank.name == bank.name).first()
        if not db_bank:
            db.add(bank)

    db.commit()


def fill_cards(db: Session):
    card_data = [
        Card(name="Silver", bank_id=2),
        Card(name="Gold", bank_id=2),
        Card(name="Platinum", bank_id=2),
        Card(name="Digital Bonus", bank_id=1),
        Card(name="#картакарта", bank_id=3),
        Card(name="#IronCard", bank_id=3),
        Card(name="#TravelCard", bank_id=3),
        Card(name="#juniorcard", bank_id=3),
        Card(name="#bccpay", bank_id=3),
        Card(name="#ҮлкенгеКұрмет", bank_id=3),
    ]

    for card in card_data:
        # Check if card already exists to avoid duplicates
        db_card = db.query(Card).filter(Card.name == card.name).first()
        if not db_card:
            db.add(card)

    db.commit()


def fill_offers(db: Session):
    offer_data = [
        Offer(
            name="Halyk QR Bonus",
            category_id=None,
            card_id=4,
            partner=None,
            condition="QR payment",
            cashback=1,
        ),
    ]

    for offer in offer_data:
        # Check if card already exists to avoid duplicates
        db_card = db.query(Offer).filter(Offer.name == offer.name).first()
        if not db_card:
            db.add(offer)

    db.commit()
