from datetime import datetime
from typing import Optional

from pydantic import BaseModel


TOKEN_TYPE = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[datetime] = None
