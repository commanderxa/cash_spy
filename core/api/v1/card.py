# Setup OAuth
from datetime import datetime
import os
from datetime import timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from core.api.dep import get_current_user, get_db
import core.schemes.card as s_card
import core.security.token as token
import core.schemes.token as token_scheme
from core.services.card import add_card, get_cards_by_bank, get_cards_by_user
import core.models.user as m_user

router = APIRouter(tags=["monitor"])


@router.get("/", response_model=list[s_card.CardResp])
async def get_all_cards_by_bank(
    bank_id: str,
    session: Session = Depends(get_db),
):
    _cards = get_cards_by_bank(db=session, bank_id=bank_id)
    cards: list[s_card.Card] = []
    if _cards:
        for c in _cards:
            cards.append(s_card.CardResp(id=c.id, name=c.name, bank_id=c.bank_id))
    return cards


@router.get("/my", response_model=list[s_card.UserCard])
async def get_my_cards(
    user = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    _cards = get_cards_by_user(db=session, user_id=user.id)
    cards: list[s_card.UserCard] = []
    if _cards:
        for c in _cards:
            print(c.card.name)
            cards.append(s_card.UserCard(user_id=c.user_id, card_id=c.card_id, bank=c.card.bank.name, card=c.card.name))
    return cards


@router.post("/add")
async def create_card(
    card: s_card.UserCardCreate,
    user: m_user.User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> token_scheme.Token:
    card = add_card(session, card.card_id, user.id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error requesting card insertion",
        )
    return Response(status_code=201)
