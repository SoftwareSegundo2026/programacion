from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class MediaType(Base):
    __tablename__ = 'MediaType'
    MediaTypeId = Column(Integer, primary_key=True)
    Name = Column(String(120))


class Track(Base):
    __tablename__ = 'Track'
    TrackId = Column(Integer, primary_key=True)
    Name = Column(String(200), nullable=False)
    AlbumId = Column(Integer, ForeignKey('Album.AlbumId'))
    MediaTypeId = Column(Integer, ForeignKey('MediaType.MediaTypeId'), nullable=False)
    GenreId = Column(Integer, ForeignKey('Genre.GenreId'))
    Composer = Column(String(220))
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2), nullable=False)

    album = relationship('Album', backref='tracks')
    media_type = relationship('MediaType', backref='tracks')
    genre = relationship('Genre', backref='tracks')

    @property
    def AlbumTitle(self) -> Optional[str]:
        return self.album.Title if self.album else None

    @property
    def GenreName(self) -> Optional[str]:
        return self.genre.Name if self.genre else None

    @property
    def MediaTypeName(self) -> Optional[str]:
        return self.media_type.Name if self.media_type else None