from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserInDB(User):
    password: str


class UserForm(BaseModel):
    username: str
    password: str