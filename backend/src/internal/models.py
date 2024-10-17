from pydantic import BaseModel

__all__ = (
    "Token",
    "TokenData",
    "UserLogin",
    "User",
    "UserData",
    "RegisteredResponse",
)

# TODO: Better naming for the models


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    refresh_token: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    password: str
    email: str
    name: str
    surname: str
    middle_name: str


class UserData(BaseModel):
    username: str
    email: str
    name: str
    surname: str
    middle_name: str


class RegisteredResponse(BaseModel):
    token: Token
    user: UserData
