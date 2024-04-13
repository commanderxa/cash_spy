# Setup OAuth
from datetime import datetime
import os
from datetime import timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from core.api.dep import get_current_user, get_db
import core.schemes.bank as s_bank
from core.services.bank import get_banks

router = APIRouter(tags=["monitor"])


@router.get("/", response_model=list[s_bank.BankResp])
async def get_all_banks(
    session: Session = Depends(get_db),
):
    _banks = get_banks(session)
    banks: list[s_bank.Bank] = []
    if _banks:
        for c in _banks:
            banks.append(
                s_bank.BankResp(id=c.id, name=c.name)
            )
    return banks


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
