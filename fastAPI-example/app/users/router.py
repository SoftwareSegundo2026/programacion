from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user
from app.auth.schemas import UserInDB
from app.auth.service import create_user, list_users
from app.core.database import get_db

from .schemas import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
async def read_users(
    _: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> list[User]:
    return await list_users(db)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_in: UserCreate,
    _: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        return await create_user(db, user_in)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error