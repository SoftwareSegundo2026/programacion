from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.service import log_activity
from app.api.dependencies import get_current_active_user, get_current_admin_user
from app.auth.schemas import UserInDB
from app.auth.service import create_user, list_users, update_user_disabled, change_password, reset_password, delete_user
from app.core.database import get_db

from .schemas import User, UserCreate, UserUpdateDisabled, PasswordChange, PasswordReset

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
async def read_users(
    _: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    return await list_users(db, skip, limit)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_in: UserCreate,
    current_user: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        user = await create_user(db, user_in)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    await log_activity(db, current_user.username, "create", f"User: {user.username}")
    return user


@router.patch("/{user_id}", response_model=User)
async def toggle_user_disabled(
    user_id: int,
    body: UserUpdateDisabled,
    current_user: UserInDB = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await update_user_disabled(db, user_id, body.disabled)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    action = "activate" if not body.disabled else "deactivate"
    await log_activity(db, current_user.username, "update", f"User {action}: {user.username} (id={user_id})")
    return user


@router.get("/me", response_model=User)
async def read_current_user(
    current_user: UserInDB = Depends(get_current_active_user),
) -> User:
    return User.model_validate(current_user)


@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_own_password(
    body: PasswordChange,
    current_user: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    ok = await change_password(db, current_user.username, body.current_password, body.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    await log_activity(db, current_user.username, "update", "Password changed")


@router.patch("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_user_password(
    user_id: int,
    body: PasswordReset,
    current_user: UserInDB = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    ok = await reset_password(db, user_id, body.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await log_activity(db, current_user.username, "update", f"Password reset for user id={user_id}")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    user_id: int,
    current_user: UserInDB = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    ok = await delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await log_activity(db, current_user.username, "delete", f"User id={user_id}")