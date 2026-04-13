from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from .schemas import Artist, ArtistCreate, ArtistUpdate
from .service import artist_service

router = APIRouter()

@router.post("/", response_model=Artist, status_code=status.HTTP_201_CREATED)
async def create_artist(
    artist_in: ArtistCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new artist."""
    artist = await artist_service.create_artist(db, artist_in)
    return artist

@router.get("/{artist_id}", response_model=Artist)
async def read_artist(
    artist_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get artist by ID."""
    artist = await artist_service.get_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.get("/", response_model=List[Artist])
async def read_artists(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get multiple artists."""
    artists = await artist_service.get_artists(db, skip, limit)
    return artists

@router.patch("/{artist_id}", response_model=Artist)
async def update_artist(
    artist_id: int,
    artist_in: ArtistUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update artist."""
    artist = await artist_service.update_artist(db, artist_id, artist_in)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(
    artist_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete artist."""
    deleted = await artist_service.delete_artist(db, artist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artist not found")