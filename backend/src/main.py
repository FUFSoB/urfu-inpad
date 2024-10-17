from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from internal import *

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(user: UserLogin) -> str | None:
    user_data = get_user_by_username(user.username)
    if not user_data:
        return None
    if not verify_password(user.password, user_data["password"]):
        return None
    return user.username


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


@app.get("/current_user", response_model=UserData)
async def get_user_data(token: str = Depends(oauth2_scheme)):
    try:
        username = verify_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user_data = get_user_by_username(username).copy()
    user_data.pop("password")
    return user_data


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
    user_data = {
        "id": users[-1]["id"] + 1,
        "username": user.username,
        "password": get_password_hash(user.password),
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "middle_name": user.middle_name,
    }
    users.append(user_data.copy())
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    user_data.pop("password")
    return {
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
        "user": user_data,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
