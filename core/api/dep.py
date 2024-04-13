from fastapi import Depends, HTTPException, security, status
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

import core.models.user as m_user
import core.schemes.token as s_token
import core.services.user as user_serv
from core.security import token as security_token
from ..database import SessionLocal


reusable_oauth2 = security.OAuth2PasswordBearer(f"api/v1/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_token(
    token: str = Depends(reusable_oauth2),
) -> tuple[str, s_token.TokenPayload]:
    """
    Checks JWT token and returns it along with claims if token is valid
    """

    try:
        payload = jwt.decode(
            token=token, key=security_token.SECRET_KEY, algorithms=security_token.ALGORITHM
        )
        token_data = s_token.TokenPayload(**payload)
    except (JWTError, ValidationError):
        print()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token, token_data


def get_current_user(
    session: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> m_user.User:
    """
    Checks JWT token and gets user based on user_id in JWT
    """

    print(token)

    try:
        payload = jwt.decode(token=token, key=security_token.SECRET_KEY, algorithms=security_token.ALGORITHM)
        print(payload)
        token_data = s_token.TokenPayload(**payload)
        print(token_data)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_serv.get_user(session, user_id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
