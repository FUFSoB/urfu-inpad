from pydantic import BaseModel

__all__ = (
    "Token",
    "TokenData",
    "UserLogin",
    "UserRegister",
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
    email: str
    password: str


class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    middle_name: str


class UserData(BaseModel):
    email: str
    name: str
    surname: str
    middle_name: str


class RegisteredResponse(BaseModel):
    token: Token
    user: UserData
