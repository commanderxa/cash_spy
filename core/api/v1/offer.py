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
from core.services.offer import add_offer
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
