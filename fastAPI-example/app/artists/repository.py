from sqlalchemy import select
from app.core.base_repository import BaseRepository
from .model import Artist
from .schemas import ArtistCreate, ArtistUpdate

class ArtistRepository(BaseRepository[Artist, ArtistCreate, ArtistUpdate]):
    """Artist-specific repository."""

    async def get_by_name(self, db, name: str):
        """Get artist by name."""
        result = await db.execute(
            select(Artist).where(Artist.Name == name)
        )
        return result.scalars().first()

artist_repository = ArtistRepository(Artist)