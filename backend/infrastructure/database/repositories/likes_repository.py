from typing import List

from sqlalchemy.orm import Session

from backend.domain.models.likes import Likes


class LikesRepository:
    @staticmethod
    def get_liked_painting_ids(account_id: int, db: Session) -> List[int]:
        liked_paintings = db.query(Likes).filter(Likes.account_id == account_id).all()
        return [like.painting_id for like in liked_paintings]

    @staticmethod
    def get_likes_count(painting_id: int, db: Session) -> int:
        return db.query(Likes).filter(Likes.painting_id == painting_id).count()