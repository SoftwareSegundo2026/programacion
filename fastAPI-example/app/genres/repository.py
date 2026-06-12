from app.core.base_repository import BaseRepository
from .model import Genre
from .schemas import Create, Update

class GenreRepository(BaseRepository[Genre, Create, Update]):
    """Repositorio de géneros. Usa el CRUD genérico sin modificaciones."""
    pass

genre_repository = GenreRepository(Genre)
