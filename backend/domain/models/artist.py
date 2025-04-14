from sqlalchemy import Column, Integer, Text, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from backend.infrastructure.database.db import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    img_path = Column(VARCHAR(255), nullable=True)
    description = Column(Text, nullable=True)
    subscribers_count = Column(Integer, default=0)

    artist_page = relationship("ArtistPage", back_populates="artist", cascade="all, delete", uselist=False)
    paintings = relationship("Painting", back_populates="artist", cascade="all, delete")
    subscribers = relationship("Subscribes", back_populates="artist", cascade="all, delete-orphan")
    account = relationship("Account", back_populates="artist", uselist=False)

    def __repr__(self):
        return f"Artist(id={self.id}, name='{self.name}')"
