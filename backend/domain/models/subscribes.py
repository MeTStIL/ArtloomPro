from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.infrastructure.database.db import Base

class Subscribes(Base):
    __tablename__ = 'subscribes'

    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), primary_key=True)

    account = relationship("Account", foreign_keys=[account_id], back_populates="subscriptions")
    artist = relationship("Artist", foreign_keys=[artist_id], back_populates="subscribers")

    def __repr__(self):
        return f"<Subscribes(account_id={self.account_id}, artist_id={self.artist_id}')>"
