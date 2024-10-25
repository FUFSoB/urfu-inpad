import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
import bcrypt

__all__ = (
    "verify_password",
    "get_password_hash",
    "check_password_strength",
    "create_token",
    "create_access_token",
    "create_refresh_token",
    "verify_token",
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


def check_password_strength(password: str) -> bool:
    return len(password) >= 8


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    return create_token(data, expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    return create_token(
        data, expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uuid: str = payload.get("sub")
        if uuid is None:
            raise ValueError("Invalid token")
        return uuid
    except JWTError:
        raise ValueError("Invalid token")
