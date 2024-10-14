from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional

app = FastAPI()

SECRET_KEY = "hgkadshtuiqweiuhtewio5uy2349o6y8itvhbwv3kb4j5yn2f390hn78tg3yw4vob4g6t37"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def check_password_strength(password: str) -> bool:
    return len(password) >= 8

users = [
    {
        "id": 0,
        "username": "user",
        "password": get_password_hash("password"),
        "email": "example@example.com",
        "name": "Юзер",
        "surname": "Юзеров",
        "middle_name": "Юзерович",
    },
]

organizations = [
    {
        "id": 0,
        "name": "Организация",
        "inn": "1234567890",
        "kpp": "123456789",
        "ogrn": "1234567890123",
        "address": "г. Москва, ул. Ленина, д. 1",
        "phone": "+7 (123) 456-78-90",
        "email": "example@example.com",
        "users": [0],
    },
]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(user: UserLogin) -> str | None:
    for u in users:
        if u["username"] == user.username and verify_password(user.password, u["password"]):
            return u["username"]
    return None

@app.post("/login", response_model=Token)
async def login_for_access_token(user: UserLogin):
    username = authenticate_user(user)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.get("/protected", response_model=SampleMessage)
async def protected_route(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    return {"message": f"Hello, {username}!"}

@app.post("/refresh", response_model=Token)
async def refresh_token_route(token: TokenData):
    username = verify_token(token.refresh_token)
    new_access_token = create_access_token(data={"sub": username})
    return {"access_token": new_access_token, "refresh_token": token["refresh_token"], "token_type": "bearer"}

@app.post("/register", response_model=RegisteredResponse)
async def register(user: User):
    if not check_password_strength(user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too weak")
    users.append({
        "id": users[-1]["id"] + 1,
        "username": user.username,
        "password": get_password_hash(user.password),
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "middle_name": user.middle_name,
    })
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"token": {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}, "user": user.model_dump()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
