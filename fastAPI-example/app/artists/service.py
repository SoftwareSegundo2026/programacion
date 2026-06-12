from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import artist_repository
from .schemas import Create, Update
from app.core.logging import get_logger

class ArtistService:
    """Lógica de negocio para artistas. Delega las operaciones de BD al repositorio."""

    def __init__(self):
        self.repository = artist_repository
        self.logger = get_logger(__name__)

    async def get_one(self, db: AsyncSession, artist_id: int):
        """Get artist by ID."""
        return await self.repository.get(db, artist_id)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get multiple artists."""
        self.logger.info("4. ArtistService.get_all - tarea=coordinar consulta de artistas - recibe token=NO, trabaja con usuario ya autenticado")
        return await self.repository.get_multi(db, skip, limit)

    async def create(self, db: AsyncSession, artist_in: Create):
        """Create new artist."""
        return await self.repository.create(db, artist_in)

    async def update(self, db: AsyncSession, artist_id: int, artist_in: Update):
        """Update artist."""
        artist = await self.repository.get(db, artist_id)
        if not artist:
            return None
        return await self.repository.update(db, artist, artist_in)

    async def delete(self, db: AsyncSession, artist_id: int) -> bool:
        """Delete artist."""
        return await self.repository.delete(db, artist_id)

artist_service = ArtistService()