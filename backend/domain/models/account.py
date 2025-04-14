from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from backend.infrastructure.database.db import Base
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_img_path = Column(VARCHAR(255), nullable=True, default=None)
    hashed_password = Column(String, nullable=False)
    login = Column(VARCHAR(255), unique=True, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)

    subscriptions = relationship("Subscribes", back_populates="account", cascade="all, delete-orphan")
    likes = relationship("Likes", back_populates="account", cascade="all, delete-orphan")
    artist = relationship("Artist", back_populates="account", uselist=False)

    def __repr__(self):
        return f"Account(id={self.id}, login='{self.login}')"


class Token(BaseModel):
    access_token: str
    token_type: str
