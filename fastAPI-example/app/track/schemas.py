from decimal import Decimal
from typing import Optional

from app.core.schemas import CustomModel


class Base(CustomModel):
    Name: str
    AlbumId: Optional[int] = None
    MediaTypeId: int
    GenreId: Optional[int] = None
    Composer: Optional[str] = None
    Milliseconds: int
    Bytes: Optional[int] = None
    UnitPrice: Decimal


class Create(Base):
    pass


class Update(CustomModel):
    Name: Optional[str] = None
    AlbumId: Optional[int] = None
    MediaTypeId: Optional[int] = None
    GenreId: Optional[int] = None
    Composer: Optional[str] = None
    Milliseconds: Optional[int] = None
    Bytes: Optional[int] = None
    UnitPrice: Optional[Decimal] = None


class Response(Base):
    TrackId: int
    AlbumTitle: Optional[str] = None
    GenreName: Optional[str] = None
    MediaTypeName: Optional[str] = None