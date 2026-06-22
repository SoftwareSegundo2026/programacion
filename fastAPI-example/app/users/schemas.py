from typing import Optional

from app.core.schemas import CustomModel


class Token(CustomModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(CustomModel):
    sub: str


class UserLogin(CustomModel):
    username: str
    password: str


class User(CustomModel):
    user_id: Optional[int] = None
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
    is_admin: bool = False


class UserInDB(User):
    hashed_password: str


class UserCreate(CustomModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: bool = False
    is_admin: bool = False
    password: str


class UserUpdateDisabled(CustomModel):
    disabled: bool


class UserUpdate(CustomModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class PasswordChange(CustomModel):
    current_password: str
    new_password: str


class PasswordReset(CustomModel):
    new_password: str
