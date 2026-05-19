from sqlalchemy import select
from app.core.base_repository import BaseRepository
from app.core.logging import get_logger
from .model import Artist
from .schemas import Create, Update

class ArtistRepository(BaseRepository[Artist, Create, Update]):
    """Artist-specific repository."""

    def __init__(self, model):
        super().__init__(model)
        self.logger = get_logger(__name__)

    async def get_multi(self, db, skip: int = 0, limit: int = 100):
        """Get multiple artists."""
        self.logger.info("5. ArtistRepository.get_multi - tarea=consultar artistas en BD - recibe token=NO, usa sesion SQLAlchemy")
        return await super().get_multi(db, skip, limit)

    async def get_by_name(self, db, name: str):
        """Get artist by name."""
        result = await db.execute(
            select(Artist).where(Artist.Name == name)
        )
        return result.scalars().first()

artist_repository = ArtistRepository(Artist)