from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from backend.infrastructure.database.db import Base


class ArtistPage(Base):
    __tablename__ = "artist_pages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), unique=True, nullable=False)

    artist = relationship("Artist", back_populates="artist_page")

    def __repr__(self):
        return f"ArtistPage(id={self.id}, url={self.url})"