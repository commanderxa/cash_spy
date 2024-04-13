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

from core.api.dep import get_db
from core.schemes.user import UserInDB
import core.security.token as token
import core.schemes.token as token_scheme
from core.services.user import create_user, get_user_by_username

router = APIRouter(tags=["monitor"])


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password


def authenticate_user(session: Session, username: str, password: str):
    user = get_user_by_username(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token.SECRET_KEY, algorithm=token.ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
) -> token_scheme.Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return token_scheme.Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(
    form_data: UserInDB,
    session: Session = Depends(get_db),
) -> token_scheme.Token:
    user = get_user_by_username(session, form_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username is taken"
        )
    create_user(
        session, UserInDB(username=form_data.username, password=form_data.password)
    )
    user = get_user_by_username(session, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error requesting token"
        )
    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return token_scheme.Token(access_token=access_token, token_type="bearer")
