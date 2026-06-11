from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.activities.service import log_activity
from app.api.dependencies import get_current_active_user
from app.core.database import get_db
from app.users.schemas import UserInDB
from .schemas import Response, Create, Update
from .service import genre_service

router = APIRouter()

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create(
    genre_in: Create,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Create new genre."""
    genre = await genre_service.create(db, genre_in)
    await log_activity(db, current_user.username, "create", f"Genre: {genre.Name} (id={genre.GenreId})")
    return genre

@router.get("/{genre_id}", response_model=Response)
async def read_one(
    genre_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get genre by ID."""
    genre = await genre_service.get_one(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@router.get("/", response_model=List[Response])
async def read_all(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get multiple genres."""
    genres = await genre_service.get_all(db, skip, limit)
    return genres

@router.patch("/{genre_id}", response_model=Response)
async def update(
    genre_id: int,
    genre_in: Update,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Update genre."""
    genre = await genre_service.update(db, genre_id, genre_in)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    await log_activity(db, current_user.username, "update", f"Genre id={genre_id}")
    return genre

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    genre_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Delete genre."""
    deleted = await genre_service.delete(db, genre_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Genre not found")
    await log_activity(db, current_user.username, "delete", f"Genre id={genre_id}")
