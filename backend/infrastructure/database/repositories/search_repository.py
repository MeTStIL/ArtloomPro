from sqlalchemy.orm import Session
from sqlalchemy import cast, Float, func
from backend.domain.models.painting import Painting
from backend.infrastructure.database.schemas.search_schemas import PaintingSearchResult

class SearchRepository:
    @staticmethod
    def search_painting_ids(text_embedding, limit: int, db: Session):
        query = (
            db.query(
                Painting.id,
                cast(Painting.img_embedding.op("<->")(text_embedding),
                     Float).label("score")
            )
            .filter(Painting.img_embedding.isnot(None))
            .order_by("score")
            .limit(limit)
        )
        results = query.all()
        return [row[0] for row in results]

    @staticmethod
    def get_random_painting_ids(limit: int, db: Session):
        query = (
            db.query(Painting.id)
            .order_by(func.random())
            .limit(limit)
        )
        results = query.all()
        return [row[0] for row in results]
