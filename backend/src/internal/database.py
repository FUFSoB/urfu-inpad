from .security import get_password_hash

__all__ = ("users",)

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
