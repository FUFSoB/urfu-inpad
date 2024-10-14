from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from internal import *

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(user: UserLogin) -> str | None:
    for u in users:
        if u["username"] == user.username and verify_password(
            user.password, u["password"]
        ):
            return u["username"]
    return None


@app.post("/login", response_model=Token)
async def login_for_access_token(user: UserLogin):
    username = authenticate_user(user)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.get("/protected", response_model=SampleMessage)
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        username = verify_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"message": f"Hello, {username}!"}


@app.post("/refresh", response_model=Token)
async def refresh_token_route(token: TokenData):
    try:
        username = verify_token(token.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    new_access_token = create_access_token(data={"sub": username})
    return {
        "access_token": new_access_token,
        "refresh_token": token.refresh_token,
        "token_type": "bearer",
    }


@app.post("/register", response_model=RegisteredResponse)
async def register(user: User):
    if not check_password_strength(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too weak"
        )
    users.append(
        {
            "id": users[-1]["id"] + 1,
            "username": user.username,
            "password": get_password_hash(user.password),
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "middle_name": user.middle_name,
        }
    )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
        "user": user.model_dump(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
