from .security import get_password_hash

__all__ = ("users","project")

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
