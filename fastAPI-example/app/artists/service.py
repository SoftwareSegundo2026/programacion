from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import artist_repository
from .schemas import Create, Update

class ArtistService:
    """Business logic for artists."""

    def __init__(self):
        self.repository = artist_repository

    async def get_one(self, db: AsyncSession, artist_id: int):
        """Get artist by ID."""
        return await self.repository.get(db, artist_id)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get multiple artists."""
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