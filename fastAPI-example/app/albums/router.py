from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.activities.service import log_activity
from app.api.dependencies import get_current_active_user
from app.core.database import get_db
from app.core.image_service import save_upload, get_image_response, fetch_from_wikipedia
from app.users.schemas import UserInDB
from .schemas import Response, Create, Update
from .service import album_service

router = APIRouter()

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create(
    album_in: Create,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """POST /albums/ - Crea un álbum (requiere auth) y registra la acción."""
    album = await album_service.create(db, album_in)
    await log_activity(db, current_user.username, "create", f"Album: {album.Title} (id={album.AlbumId})")
    return album

@router.get("/{album_id}", response_model=Response)
async def read_one(
    album_id: int,
    db: AsyncSession = Depends(get_db)
):
    """GET /albums/{id} - Devuelve un álbum por ID. Público."""
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
    """GET /albums/ - Devuelve lista paginada de álbumes. Público."""
    albums = await album_service.get_all(db, skip, limit)
    return albums

@router.patch("/{album_id}", response_model=Response)
async def update(
    album_id: int,
    album_in: Update,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """PATCH /albums/{id} - Actualiza un álbum (requiere auth) y registra la acción."""
    album = await album_service.update(db, album_id, album_in)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    await log_activity(db, current_user.username, "update", f"Album id={album_id}")
    return album

@router.post("/{album_id}/image", response_model=Response)
async def upload_image(
    album_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: UserInDB = Depends(get_current_active_user),
):
    """POST /albums/{id}/image - Sube una imagen para el álbum."""
    album = await album_service.get_one(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    image_url = await save_upload("albums", album_id, file)
    album.ImageUrl = image_url
    await db.flush()
    return album


@router.get("/{album_id}/image")
async def get_image(
    album_id: int,
    db: AsyncSession = Depends(get_db),
):
    """GET /albums/{id}/image - Devuelve la imagen del álbum o un placeholder por defecto."""
    album = await album_service.get_one(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return get_image_response(album.ImageUrl, entity_type="albums")


@router.post("/{album_id}/fetch-image", response_model=Response)
async def fetch_image(
    album_id: int,
    db: AsyncSession = Depends(get_db),
    _: UserInDB = Depends(get_current_active_user),
):
    """POST /albums/{id}/fetch-image - Busca una imagen en Wikipedia y la asigna al álbum."""
    album = await album_service.get_one(db, album_id)
    if not album or not album.Title:
        raise HTTPException(status_code=404, detail="Album not found or has no title")
    image_url = await fetch_from_wikipedia("albums", album_id, album.Title)
    album.ImageUrl = image_url
    await db.flush()
    return album


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    album_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """DELETE /albums/{id} - Elimina un álbum (requiere auth) y registra la acción."""
    deleted = await album_service.delete(db, album_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Album not found")
    await log_activity(db, current_user.username, "delete", f"Album id={album_id}")
