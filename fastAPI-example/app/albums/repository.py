from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.core.base_repository import BaseRepository
from .model import Album
from .schemas import Create, Update

class AlbumRepository(BaseRepository[Album, Create, Update]):
    """Album-specific repository."""

    async def get(self, db, id: int):
        """Get album by ID with artist name."""
        result = await db.execute(
            select(Album)
            .options(joinedload(Album.artist))
            .where(Album.AlbumId == id)
        )
        return result.scalars().first()

    async def get_multi(self, db, skip: int = 0, limit: int = 100):
        """Get multiple albums with artist name."""
        result = await db.execute(
            select(Album)
            .options(joinedload(Album.artist))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

album_repository = AlbumRepository(Album)
