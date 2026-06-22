from __future__ import annotations

from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Album(Base):
    __tablename__ = 'Album'
    AlbumId: Mapped[int] = mapped_column(primary_key=True)
    Title: Mapped[str] = mapped_column(String(160), nullable=False)
    ArtistId: Mapped[int] = mapped_column(ForeignKey('Artist.ArtistId'), nullable=False)
    ImageUrl: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    artist: Mapped[Artist] = relationship(back_populates="albums")

    @property
    def ArtistName(self) -> str | None:
        return self.artist.Name if self.artist else None
