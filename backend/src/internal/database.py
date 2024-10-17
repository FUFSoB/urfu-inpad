from .security import get_password_hash
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, FastAPI, HTTPException, Query
from typing import Annotated

__all__ = ("users", "project", "get_user_by_username")

# TODO: Replace with real database

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

project = [
    {
        "name": "Пассаж2",
        "location": 0,
        "type": "Торговый центр",
        "square": 12,
    }
]

<<<<<<< HEAD
class User (SQLModel, table = True):
    id:int | None = Field(default=None, index=True)
    username:str = Field(index=True)
    password:str = Field(index=True)
    email:str = Field(index=True)
    name:str = Field(index=True)
    surname:str = Field(index=True)
    middle_name:str = Field(index=True)

pgsql_file_name = "database.db"
pgsql_url = f"pgsql:///{pgsql_file_name}"

connect_args = {"check_same":False}
engine = create_engine(pgsql_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
=======

def get_user_by_username(username: str) -> dict:
    for user in users:
        if user["username"] == username:
            return user
    return None
>>>>>>> 368224eed1e237e0e4762ad803d12ef14109ea08
