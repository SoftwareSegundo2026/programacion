from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.base_repository import BaseRepository

from .model import Track
from .schemas import Create, Update


class TrackRepository(BaseRepository[Track, Create, Update]):
    """Repositorio de tracks. Carga también los datos relacionados (álbum, género, tipo de medio)."""

    async def create(self, db, obj_in: Create):
        """Create track and reload it with relationships."""
        track = await super().create(db, obj_in)
        return await self.get(db, track.TrackId)

    async def get(self, db, id: int):
        """Get track by ID with related names."""
        result = await db.execute(
            select(Track)
            .options(
                joinedload(Track.album),
                joinedload(Track.genre),
                joinedload(Track.media_type),
            )
            .where(Track.TrackId == id)
        )
        return result.scalars().first()

    async def get_multi(self, db, skip: int = 0, limit: int = 100):
        """Get multiple tracks with related names."""
        result = await db.execute(
            select(Track)
            .options(
                joinedload(Track.album),
                joinedload(Track.genre),
                joinedload(Track.media_type),
            )
            .order_by(Track.TrackId)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


track_repository = TrackRepository(Track)