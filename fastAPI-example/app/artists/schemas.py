from app.core.schemas import CustomModel
from typing import Optional

class Base(CustomModel):
    Name: str
    ImageUrl: Optional[str] = None

class Create(Base):
    pass

class Update(Base):
    Name: Optional[str] = None

class Response(Base):
    ArtistId: int