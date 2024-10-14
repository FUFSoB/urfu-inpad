from pydantic import BaseModel

__all__ = (
    "Token",
    "TokenData",
    "UserLogin",
    "User",
    "SampleMessage",
    "RegisteredResponse",
)


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


class SampleMessage(BaseModel):
    message: str


class RegisteredResponse(BaseModel):
    token: Token
    user: User
