from datetime import timedelta
from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.model import User as UserModel
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.core.security import create_access_token, get_password_hash, verify_password

from .schemas import User, UserCreate, UserInDB

settings = get_settings()


async def get_user(db: AsyncSession | None, username: str) -> Optional[UserInDB]:
    if db is None:
        async with AsyncSessionLocal() as session:
            return await get_user(session, username)

    result = await db.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    if user is None:
        return None
    return UserInDB.model_validate(user)


async def authenticate_user(db: AsyncSession | None, username: str, password: str) -> Optional[UserInDB]:
    user = await get_user(db, username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def list_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(
        select(UserModel).order_by(UserModel.user_id).offset(skip).limit(limit)
    )
    return [User.model_validate(user) for user in result.scalars().all()]


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    result = await db.execute(
        select(UserModel).where(
            or_(
                UserModel.username == user_in.username,
                UserModel.email == user_in.email,
            )
        )
    )
    if result.scalars().first() is not None:
        raise ValueError("username or email already exists")

    db_user = UserModel(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        disabled=user_in.disabled,
        is_admin=user_in.is_admin,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return User.model_validate(db_user)


async def update_user_disabled(db: AsyncSession, user_id: int, disabled: bool) -> User | None:
    result = await db.execute(select(UserModel).where(UserModel.user_id == user_id))
    user = result.scalars().first()
    if user is None:
        return None
    user.disabled = disabled
    await db.flush()
    await db.refresh(user)
    return User.model_validate(user)


async def change_password(
    db: AsyncSession,
    username: str | None,
    current_password: str,
    new_password: str,
    user_id: int | None = None,
) -> bool:
    if user_id is not None:
        result = await db.execute(select(UserModel).where(UserModel.user_id == user_id))
    elif username is not None:
        result = await db.execute(select(UserModel).where(UserModel.username == username))
    else:
        return False
    user = result.scalars().first()
    if user is None:
        return False
    if not verify_password(current_password, user.hashed_password):
        return False
    user.hashed_password = get_password_hash(new_password)
    await db.flush()
    return True


def create_user_access_token(user: UserInDB) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token({"sub": user.username}, expires_delta=expires_delta)


async def reset_password(db: AsyncSession, user_id: int, new_password: str) -> bool:
    result = await db.execute(select(UserModel).where(UserModel.user_id == user_id))
    user = result.scalars().first()
    if user is None:
        return False
    user.hashed_password = get_password_hash(new_password)
    await db.flush()
    return True


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(UserModel).where(UserModel.user_id == user_id))
    user = result.scalars().first()
    if user is None:
        return False
    await db.delete(user)
    return True