from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from .schemas import Response, Create, Update
from .service import album_service

router = APIRouter()

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create(
    album_in: Create,
    db: AsyncSession = Depends(get_db)
):
    """Create new album."""
    album = await album_service.create(db, album_in)
    return album

@router.get("/{album_id}", response_model=Response)
async def read_one(
    album_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get album by ID."""
    album = await album_service.get_one(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.get("/", response_model=List[Response])
async def read_all(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get multiple albums."""
    albums = await album_service.get_all(db, skip, limit)
    return albums

@router.patch("/{album_id}", response_model=Response)
async def update(
    album_id: int,
    album_in: Update,
    db: AsyncSession = Depends(get_db)
):
    """Update album."""
    album = await album_service.update(db, album_id, album_in)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    album_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete album."""
    deleted = await album_service.delete(db, album_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Album not found")
