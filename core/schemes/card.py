from pydantic import BaseModel


class Card(BaseModel):
    bank_id: int
    name: str


class CardResp(Card):
    id: int


class UserCard(BaseModel):
    user_id: int
    card_id: int
    bank: str
    card: str


class UserCardCreate(BaseModel):
    card_id: int
