from app.core.base_repository import BaseRepository
from .model import Genre
from .schemas import Create, Update

class GenreRepository(BaseRepository[Genre, Create, Update]):
    """Genre-specific repository."""
    pass

genre_repository = GenreRepository(Genre)
