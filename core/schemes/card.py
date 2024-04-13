from pydantic import BaseModel


class Card(BaseModel):
    user_id: int
    bank_id: int
    name: str

class CardResp(Card):
    id: int