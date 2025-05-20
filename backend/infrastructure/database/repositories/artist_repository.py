from typing import Optional

from sqlalchemy.orm import Session

from backend.domain.models.account import Account
from backend.domain.models.artist import Artist
from backend.infrastructure.database.schemas.artist_schemas import ArtistCreate, ArtistPublic

class ArtistRepository:
    @staticmethod
    def create_artist(artist: ArtistCreate, db: Session) -> ArtistPublic:
        artist_data = artist.model_dump(exclude_unset=True)
        new_artist = Artist(**artist_data)
        db.add(new_artist)
        db.commit()
        db.refresh(new_artist)
        return ArtistPublic.model_validate(new_artist)

    @staticmethod
    def get_artist_by_id(artist_id: int, db: Session) -> Optional[ArtistPublic]:
        artist = db.query(Artist).filter_by(id=artist_id).first()
        if not artist:
            return None
        return ArtistPublic.model_validate(artist)

    @staticmethod
    def delete_artist(id: int, db: Session) -> bool:
        artist = db.query(Artist).filter_by(id=id).first()
        if artist:
            db.delete(artist)
            db.commit()
            return True
        return False

    @staticmethod
    def update_artist(artist_id: int, new_artist_dict: dict, db: Session) -> Optional[ArtistPublic]:
        artist = db.query(Artist).filter_by(id=artist_id).first()
        if not artist:
            return None

        for key, value in new_artist_dict.items():
            setattr(artist, key, value)

        db.commit()
        db.refresh(artist)
        return ArtistPublic.model_validate(artist)

    @staticmethod
    def get_artist_by_account_id(account_id: int, db: Session) -> Optional[ArtistPublic]:
        artist = db.query(Account).filter_by(id=account_id).first().artist
        if not artist:
            return None
        return ArtistPublic.model_validate(artist)


