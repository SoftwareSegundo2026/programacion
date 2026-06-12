from sqlalchemy.ext.asyncio import AsyncSession

from .repository import track_repository
from .schemas import Create, Update


class TrackService:
    """Lógica de negocio para tracks. Delega las operaciones de BD al repositorio."""

    def __init__(self):
        self.repository = track_repository

    async def get_one(self, db: AsyncSession, track_id: int):
        """Get track by ID."""
        return await self.repository.get(db, track_id)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get multiple tracks."""
        return await self.repository.get_multi(db, skip, limit)

    async def create(self, db: AsyncSession, track_in: Create):
        """Create new track."""
        return await self.repository.create(db, track_in)

    async def update(self, db: AsyncSession, track_id: int, track_in: Update):
        """Update track."""
        track = await self.repository.get(db, track_id)
        if not track:
            return None
        return await self.repository.update(db, track, track_in)

    async def delete(self, db: AsyncSession, track_id: int) -> bool:
        """Delete track."""
        return await self.repository.delete(db, track_id)


track_service = TrackService()