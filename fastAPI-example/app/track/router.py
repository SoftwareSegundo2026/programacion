from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.activities.service import log_activity
from app.api.dependencies import get_current_active_user
from app.core.database import get_db
from app.users.schemas import UserInDB

from .schemas import Response, Create, Update
from .service import track_service

router = APIRouter()


@router.post("", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create(
    track_in: Create,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Create new track."""
    track = await track_service.create(db, track_in)
    await log_activity(db, current_user.username, "create", f"Track: {track.Name} (id={track.TrackId})")
    return track


@router.get("/{track_id}", response_model=Response)
async def read_one(
    track_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get track by ID."""
    track = await track_service.get_one(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.get("", response_model=List[Response])
async def read_all(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get multiple tracks."""
    tracks = await track_service.get_all(db, skip, limit)
    return tracks


@router.patch("/{track_id}", response_model=Response)
async def update(
    track_id: int,
    track_in: Update,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Update track."""
    track = await track_service.update(db, track_id, track_in)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    await log_activity(db, current_user.username, "update", f"Track id={track_id}")
    return track


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    track_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Delete track."""
    deleted = await track_service.delete(db, track_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Track not found")
    await log_activity(db, current_user.username, "delete", f"Track id={track_id}")
