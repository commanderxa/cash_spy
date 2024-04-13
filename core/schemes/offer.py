from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Assuming you have or will create similar Pydantic models for Category and other related models
class CategoryBase(BaseModel):
    id: int
    name: str

class OfferBase(BaseModel):
    id: int
    name: str
    category_id: int
    card_id: Optional[int] = None
    partner_id: Optional[int] = None
    description: Optional[str] = None
    condition: Optional[str] = None
    cashback: float
    favorite_cashback: Optional[float] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class OfferCreate(BaseModel):
    name: str
    category_id: int
    card_id: Optional[int] = None
    partner_id: Optional[int] = None
    description: Optional[str] = None
    condition: Optional[str] = None
    cashback: float
    favorite_cashback: Optional[float] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class Offer(OfferBase):
    category: CategoryBase
