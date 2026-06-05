from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.activities.service import log_activity
from app.api.dependencies import get_current_active_user
from app.core.database import get_db
from app.core.logging import get_logger
from app.core.image_service import save_upload, get_image_response, fetch_from_wikipedia
from app.auth.schemas import UserInDB
from .schemas import Response, Create, Update
from .service import artist_service

router = APIRouter()
logger = get_logger(__name__)

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create(
    artist_in: Create,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Create new artist."""
    artist = await artist_service.create(db, artist_in)
    await log_activity(db, current_user.username, "create", f"Artist: {artist.Name} (id={artist.ArtistId})")
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
    logger.info("3. artists.read_all - tarea=recibir GET /artists y delegar al service")
    artists = await artist_service.get_all(db, skip, limit)
    logger.info("6. artists.read_all - tarea=retornar artistas al cliente - cantidad=%s", len(artists))
    return artists

@router.patch("/{artist_id}", response_model=Response)
async def update(
    artist_id: int,
    artist_in: Update,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Update artist."""
    artist = await artist_service.update(db, artist_id, artist_in)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    await log_activity(db, current_user.username, "update", f"Artist id={artist_id}")
    return artist

@router.post("/{artist_id}/image", response_model=Response)
async def upload_image(
    artist_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: UserInDB = Depends(get_current_active_user),
):
    """Upload an image for the artist."""
    artist = await artist_service.get_one(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    image_url = await save_upload("artists", artist_id, file)
    artist.ImageUrl = image_url
    await db.flush()
    return artist


@router.get("/{artist_id}/image")
async def get_image(
    artist_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the artist's image file or a default placeholder."""
    artist = await artist_service.get_one(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return get_image_response(artist.ImageUrl, entity_type="artists")


@router.post("/{artist_id}/fetch-image", response_model=Response)
async def fetch_image(
    artist_id: int,
    db: AsyncSession = Depends(get_db),
    _: UserInDB = Depends(get_current_active_user),
):
    """Search Wikipedia for an image and assign it to the artist."""
    artist = await artist_service.get_one(db, artist_id)
    if not artist or not artist.Name:
        raise HTTPException(status_code=404, detail="Artist not found or has no name")
    image_url = await fetch_from_wikipedia("artists", artist_id, artist.Name)
    artist.ImageUrl = image_url
    await db.flush()
    return artist


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    artist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Delete artist."""
    deleted = await artist_service.delete(db, artist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artist not found")
    await log_activity(db, current_user.username, "delete", f"Artist id={artist_id}")
