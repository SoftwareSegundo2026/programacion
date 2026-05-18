from datetime import timedelta
from typing import Optional

from app.core.config import get_settings
from app.core.security import create_access_token, get_password_hash, verify_password

from .schemas import UserInDB

settings = get_settings()

fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Demo Admin",
        "disabled": False,
        "hashed_password": get_password_hash("admin123"),
    },
    "reader": {
        "username": "reader",
        "email": "reader@example.com",
        "full_name": "Demo Reader",
        "disabled": True,
        "hashed_password": get_password_hash("reader123"),
    },
}


def get_user(username: str) -> Optional[UserInDB]:
    user_data = fake_users_db.get(username)
    if user_data is None:
        return None
    return UserInDB(**user_data)


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_access_token(user: UserInDB) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token({"sub": user.username}, expires_delta=expires_delta)