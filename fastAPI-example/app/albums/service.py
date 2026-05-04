from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import album_repository
from .schemas import Create, Update

class AlbumService:
    """Business logic for albums."""

    def __init__(self):
        self.repository = album_repository

    async def get_one(self, db: AsyncSession, album_id: int):
        """Get album by ID."""
        return await self.repository.get(db, album_id)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get multiple albums."""
        return await self.repository.get_multi(db, skip, limit)

    async def create(self, db: AsyncSession, album_in: Create):
        """Create new album."""
        return await self.repository.create(db, album_in)

    async def update(self, db: AsyncSession, album_id: int, album_in: Update):
        """Update album."""
        album = await self.repository.get(db, album_id)
        if not album:
            return None
        return await self.repository.update(db, album, album_in)

    async def delete(self, db: AsyncSession, album_id: int) -> bool:
        """Delete album."""
        return await self.repository.delete(db, album_id)

album_service = AlbumService()
