from app.core.schemas import CustomModel
from typing import Optional

class Base(CustomModel):
    Name: str

class Create(Base):
    pass

class Update(CustomModel):
    Name: Optional[str] = None

class Response(Base):
    GenreId: int
