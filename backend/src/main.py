from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from internal import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield  # before startup ← / → after shutdown


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(user: UserLogin) -> User | None:
    user_data = await get_user_by_email(user.email)
    if not user_data:
        return None
    if not verify_password(user.password, user_data.password):
        return None
    return user_data


@app.post("/login", response_model=Token)
async def login_for_access_token(user: UserLogin):
    user_data = await authenticate_user(user)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": user_data.uuid})
    refresh_token = create_refresh_token(data={"sub": user_data.uuid})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.get("/current_user", response_model=UserData)
async def get_user_data(token: str = Depends(oauth2_scheme)):
    try:
        uuid = verify_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user_data = await get_user_by_uuid(uuid)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {
        "email": user_data.email,
        "name": user_data.name,
        "surname": user_data.surname,
        "middle_name": user_data.middle_name,
    }


@app.post("/refresh", response_model=Token)
async def refresh_token_route(token: TokenData):
    try:
        uuid = verify_token(token.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    new_access_token = create_access_token(data={"sub": uuid})
    return {
        "access_token": new_access_token,
        "refresh_token": token.refresh_token,
        "token_type": "bearer",
    }


@app.post("/register", response_model=RegisteredResponse)
async def register(user: UserRegister, session: AsyncSession = Depends(get_session)):
    if not check_password_strength(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too weak"
        )
    if got_user := await get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    # create user db record
    user_data = User(
        uuid=str(uuid4()),
        email=user.email,
        password=get_password_hash(user.password),
        name=user.name,
        surname=user.surname,
        middle_name=user.middle_name,
    )
    session.add(user_data)
    await session.commit()
    # create tokens
    access_token = create_access_token(data={"sub": user_data.uuid})
    refresh_token = create_refresh_token(data={"sub": user_data.uuid})
    return {
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
        "user": {
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "middle_name": user.middle_name,
        },
    }


@app.delete("/current_user")
async def delete_user(token: str = Depends(oauth2_scheme)):
    try:
        uuid = verify_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user_data = await get_user_by_uuid(uuid)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    async with await get_session() as session:
        await session.delete(user_data)
        await session.commit()
    return {"detail": "User deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
