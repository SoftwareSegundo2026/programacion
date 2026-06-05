from app.auth.schemas import User, UserCreate
from app.core.schemas import CustomModel

__all__ = ["User", "UserCreate", "UserUpdateDisabled", "PasswordChange", "PasswordReset"]


class UserUpdateDisabled(CustomModel):
    disabled: bool


class PasswordChange(CustomModel):
    current_password: str
    new_password: str


class PasswordReset(CustomModel):
    new_password: str