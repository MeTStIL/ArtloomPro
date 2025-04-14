from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, Text, ForeignKey, ARRAY, String
from backend.infrastructure.database.db import Base
from sqlalchemy.orm import relationship


class Painting(Base):
    __tablename__ = "paintings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=True)
    img_path = Column(Text, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    img_embedding = Column(Vector(512), nullable=True)
    img_tags = Column(ARRAY(String), nullable=True)

    artist = relationship("Artist", back_populates="paintings")
    likes = relationship("Likes", back_populates="painting", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Painting(id={self.id}')"
