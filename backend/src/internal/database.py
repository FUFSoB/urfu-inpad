from .security import get_password_hash

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


def get_user_by_username(username: str) -> dict:
    for user in users:
        if user["username"] == username:
            return user
    return None
