from app.core.schemas import CustomModel
from typing import Optional

class ArtistBase(CustomModel):
    Name: str

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(ArtistBase):
    Name: Optional[str] = None

class Artist(ArtistBase):
    ArtistId: int