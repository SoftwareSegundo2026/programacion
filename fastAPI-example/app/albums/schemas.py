from app.core.schemas import CustomModel
from typing import Optional

class Base(CustomModel):
    Title: str
    ArtistId: int
    ImageUrl: Optional[str] = None

class Create(Base):
    pass

class Update(CustomModel):
    Title: Optional[str] = None
    ArtistId: Optional[int] = None
    ImageUrl: Optional[str] = None

class Response(Base):
    AlbumId: int
    ArtistName: Optional[str] = None
