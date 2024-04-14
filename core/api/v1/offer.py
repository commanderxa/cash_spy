# Setup OAuth
from datetime import datetime
import os
from datetime import timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from core.api.dep import get_current_user, get_db
from core.ml.main import item_to_category
import core.schemes.card as s_card
import core.security.token as token
import core.schemes.token as token_scheme
import core.models.user as m_user
from core.services.bank import get_bank
from core.services.card import get_card
from core.services.offer import (
    add_offer,
    get_offers_by_bank_cards,
    get_offers_by_category,
    get_offers_by_place,
)
import core.models.offer as m_offer
import core.schemes.offer as s_offer


router = APIRouter(tags=["monitor"])


@router.post("/")
async def create_offer(
    offer: s_offer.OfferCreate,
    session: Session = Depends(get_db),
):
    offer = add_offer(offer=offer, db=session)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error adding offer"
        )

    return Response(status_code=201)


@router.get("/best")
async def get_offers(
    place: str,
    item: str,
    session: Session = Depends(get_db),
    user: m_user.User = Depends(get_current_user),
):
    offers: list[s_offer.Offer] = []
    if place and len(place) > 0:
        _offers = get_offers_by_place(place=place, db=session)
        for offer in _offers:
            _card = get_card(session, offer.card_id)
            if _card:
                card_name = _card.name
                bank_name = get_bank(session, _card.bank_id).name
            else:
                bank_name = get_bank()
            offers.append(
                s_offer.OfferBase(
                    id=offer.id,
                    name=offer.name,
                    category_id=offer.category_id,
                    card_id=offer.card_id,
                    card=card_name,
                    bank=bank_name,
                    partner=offer.partner,
                    description=offer.description,
                    condition=offer.condition,
                    cashback=offer.cashback,
                    favorite_cashback=offer.favorite_cashback,
                    date_from=offer.date_from,
                    date_to=offer.date_to,
                )
            )

    if item and len(item) > 0:
        offers_cat = get_offers_by_category(
            category=item_to_category(item), user_id=user.id, db=session
        )
        print(offers_cat)
        if offers_cat:
            for c in offers_cat:
                offers.append(
                    s_offer.Offer(
                        id=c.id,
                        name=c.name,
                        category_id=c.category_id,
                        card_id=c.card_id,
                        partner=c.partner,
                        description=c.description,
                        condition=c.condition,
                        cashback=c.cashback,
                        favorite_cashback=c.favorite_cashback,
                        date_from=c.date_from,
                        date_to=c.date_to,
                        category=None,
                    )
                )

    offers_gen = get_offers_by_bank_cards(user_id=user.id, db=session)
    if offers_gen:
        for c in offers_gen:
            offers.append(
                s_offer.Offer(
                    id=c.id,
                    name=c.name,
                    category_id=c.category_id,
                    card_id=c.card_id,
                    partner=c.partner,
                    description=c.description,
                    condition=c.condition,
                    cashback=c.cashback,
                    favorite_cashback=c.favorite_cashback,
                    date_from=c.date_from,
                    date_to=c.date_to,
                    category=None,
                )
            )

    return offers


# @router.post("/add")
# async def register(
#     form_data: s_card.Card,
#     session: Session = Depends(get_db),
# ) -> token_scheme.Token:
#     user = get_user_by_username(session, form_data.username)
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Username is taken"
#         )
#     create_user(
#         session, UserInDB(username=form_data.username, password=form_data.password)
#     )
#     user = get_user_by_username(session, form_data.username)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Error requesting token"
#         )
#     access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return token_scheme.Token(access_token=access_token, token_type="bearer")
