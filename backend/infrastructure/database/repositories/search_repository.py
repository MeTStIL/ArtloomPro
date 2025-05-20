from sqlalchemy.orm import Session
from sqlalchemy import cast, Float, func, text
from backend.domain.models.painting import Painting

class SearchRepository:
    @staticmethod
    def search_painting_ids_by_image(text_embedding, limit: int, db: Session):
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
    def search_painting_ids_by_description(description: str, limit: int, db: Session):
        words = description.split()
        long_words = [word for word in words if len(word) > 3]
        sql = text("""
                        SELECT id, description, img_path, artist_id, ts_rank(to_tsvector('russian', description), to_tsquery('russian', :query)) AS rank
                        FROM paintings
                        WHERE to_tsvector('russian', description) @@ to_tsquery('russian', :query)
                        ORDER BY rank DESC
                        LIMIT :limit;
                    """)
        results = db.execute(sql, {
            "limit": limit,
            "query": " | ".join(long_words)
        }).fetchall()

        return [row[0] for row in results[:limit]]

    @staticmethod
    def get_random_painting_ids(limit: int, db: Session):
        query = (
            db.query(Painting.id)
            .order_by(func.random())
            .limit(limit)
        )
        results = query.all()
        return [row[0] for row in results]
