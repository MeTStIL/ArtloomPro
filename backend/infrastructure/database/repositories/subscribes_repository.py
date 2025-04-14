from sqlalchemy.orm import Session

from backend.domain.models.subscribes import Subscribes


class SubscribesRepository:
    @staticmethod
    def get_subscribed_artist_ids(account_id: int, db: Session):
        subscribed_artist_ids = db.query(Subscribes).filter(Subscribes.account_id == account_id).all()
        return [sub.artist_id for sub in subscribed_artist_ids]

    @staticmethod
    def get_subscribers_count(artist_id: int, db: Session) -> int:
        return db.query(Subscribes).filter(Subscribes.artist_id == artist_id).count()
