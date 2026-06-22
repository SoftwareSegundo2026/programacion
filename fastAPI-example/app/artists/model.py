from __future__ import annotations

from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Artist(Base):
    __tablename__ = 'Artist'
    ArtistId: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(120))
    ImageUrl: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    albums: Mapped[list[Album]] = relationship(back_populates="artist")