from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from .schemas import Response, Create, Update
from .service import artist_service

router = APIRouter()

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create(
    artist_in: Create,
    db: AsyncSession = Depends(get_db)
):
    """Create new artist."""
    artist = await artist_service.create(db, artist_in)
    return artist

@router.get("/{artist_id}", response_model=Response)
async def read_one(
    artist_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get artist by ID."""
    artist = await artist_service.get_one(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.get("/", response_model=List[Response])
async def read_all(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get multiple artists."""
    artists = await artist_service.get_all(db, skip, limit)
    return artists

@router.patch("/{artist_id}", response_model=Response)
async def update(
    artist_id: int,
    artist_in: Update,
    db: AsyncSession = Depends(get_db)
):
    """Update artist."""
    artist = await artist_service.update(db, artist_id, artist_in)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    artist_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete artist."""
    deleted = await artist_service.delete(db, artist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artist not found")