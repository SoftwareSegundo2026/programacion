from pydantic import BaseModel
from typing import Optional

class ArtistBase(BaseModel):
    Name: str

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(ArtistBase):
    Name: Optional[str] = None

class Artist(ArtistBase):
    ArtistId: int

    class Config:
        from_attributes = True