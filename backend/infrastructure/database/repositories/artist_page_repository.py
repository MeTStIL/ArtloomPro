from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from backend.config import SITE_BASE_URL
from backend.domain.models.account import Account
from backend.domain.models.artist import Artist
from backend.domain.models.artist_page import ArtistPage
from backend.domain.models.painting import Painting
from backend.infrastructure.database.schemas.artist_page_schemas import ArtistPagePublic


class ArtistPageRepository:
    @staticmethod
    def create_artist_page(
            artist_id: int,
            db: Session = None
    ) -> ArtistPagePublic:
        artist_page = ArtistPage(artist_id=artist_id)

        db.add(artist_page)
        db.commit()
        db.refresh(artist_page)

        return ArtistPagePublic.model_validate(artist_page)

    @staticmethod
    def get_artist_page_by_id(id: int, db: Session) -> Optional[ArtistPagePublic]:
        artist_page = db.query(ArtistPage).filter(ArtistPage.id == id).first()
        if not artist_page:
            return None
        return ArtistPagePublic.model_validate(artist_page)

    @staticmethod
    def get_artist_page_by_login(login: str, db: Session) -> Optional[ArtistPagePublic]:
        artist_page = (
            db.query(ArtistPage)
            .join(Artist, Artist.id == ArtistPage.artist_id)
            .join(Account, Account.artist_id == Artist.id)
            .filter(Account.login == login)
            .first()
        )
        if not artist_page:
            return None
        return ArtistPagePublic.model_validate(artist_page)

    @staticmethod
    def delete_artist_page(artist_page_id: int, db: Session) -> bool:
        artist_page = db.query(ArtistPage).filter(ArtistPage.id == artist_page_id).first()
        if artist_page:
            db.delete(artist_page)
            db.commit()
            return True
        return False

    @staticmethod
    def get_artist_page_by_artist_id(artist_id: int, db: Session) -> ArtistPagePublic:
        artist_page = db.query(ArtistPage).filter(ArtistPage.artist_id == artist_id).first()
        return ArtistPagePublic.model_validate(artist_page)

    @staticmethod
    def get_painting_ids(artist_id: int, db: Session) -> List[int]:
        paintings = (db.query(Painting)
                     .filter(Painting.artist_id == artist_id)
                     .order_by(Painting.id.desc())
                     .all())
        return [painting.id for painting in paintings]

    @staticmethod
    def get_url_by_artist_id(artist_id: int, db: Session) -> str:
        artist = db.query(Artist).filter_by(id=artist_id).first()
        return f"{SITE_BASE_URL}/{artist.account.login}"
