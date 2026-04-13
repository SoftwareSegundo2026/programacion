from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Artist(Base):
    __tablename__ = 'Artist'
    ArtistId = Column(Integer, primary_key=True)
    Name = Column(String(120))