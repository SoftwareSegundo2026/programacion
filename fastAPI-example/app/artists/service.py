from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import artist_repository
from .schemas import ArtistCreate, ArtistUpdate, Artist

class ArtistService:
    """Business logic for artists."""

    def __init__(self):
        self.repository = artist_repository

    async def get_artist(self, db: AsyncSession, artist_id: int) -> Optional[Artist]:
        """Get artist by ID."""
        return await self.repository.get(db, artist_id)

    async def get_artists(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Artist]:
        """Get multiple artists."""
        return await self.repository.get_multi(db, skip, limit)

    async def create_artist(self, db: AsyncSession, artist_in: ArtistCreate) -> Artist:
        """Create new artist."""
        return await self.repository.create(db, artist_in)

    async def update_artist(self, db: AsyncSession, artist_id: int, artist_in: ArtistUpdate) -> Optional[Artist]:
        """Update artist."""
        artist = await self.repository.get(db, artist_id)
        if not artist:
            return None
        return await self.repository.update(db, artist, artist_in)

    async def delete_artist(self, db: AsyncSession, artist_id: int) -> bool:
        """Delete artist."""
        return await self.repository.delete(db, artist_id)

artist_service = ArtistService()