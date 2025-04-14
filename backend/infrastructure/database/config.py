from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain.models.account import Account
from backend.domain.models.artist_page import ArtistPage
from backend.domain.models.painting import Painting
from backend.domain.models.subscribes import Subscribes
from backend.domain.models.likes import Likes
from backend.domain.models.artist import Artist
from backend.infrastructure.database.db import Base
from backend.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
