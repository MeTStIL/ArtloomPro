from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.infrastructure.database.db import Base

class Likes(Base):
    __tablename__ = 'likes'

    account_id = Column(Integer, ForeignKey('accounts.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    painting_id = Column(Integer, ForeignKey('paintings.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    account = relationship("Account", back_populates="likes")
    painting = relationship("Painting", back_populates="likes")

    def __repr__(self):
        return f"Likes(account_id={self.account_id}, painting_id={self.painting_id})"
