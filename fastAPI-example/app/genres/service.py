from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import genre_repository
from .schemas import Create, Update

class GenreService:
    """Business logic for genres."""

    def __init__(self):
        self.repository = genre_repository

    async def get_one(self, db: AsyncSession, genre_id: int):
        """Get genre by ID."""
        return await self.repository.get(db, genre_id)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get multiple genres."""
        return await self.repository.get_multi(db, skip, limit)

    async def create(self, db: AsyncSession, genre_in: Create):
        """Create new genre."""
        return await self.repository.create(db, genre_in)

    async def update(self, db: AsyncSession, genre_id: int, genre_in: Update):
        """Update genre."""
        genre = await self.repository.get(db, genre_id)
        if not genre:
            return None
        return await self.repository.update(db, genre, genre_in)

    async def delete(self, db: AsyncSession, genre_id: int) -> bool:
        """Delete genre."""
        return await self.repository.delete(db, genre_id)

genre_service = GenreService()
