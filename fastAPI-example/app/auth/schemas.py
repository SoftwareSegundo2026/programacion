from typing import Optional

from app.core.schemas import CustomModel


class Token(CustomModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(CustomModel):
    sub: Optional[str] = None


class UserLogin(CustomModel):
    username: str
    password: str


class User(CustomModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False


class UserInDB(User):
    hashed_password: str