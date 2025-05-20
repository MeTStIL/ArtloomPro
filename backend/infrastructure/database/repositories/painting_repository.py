from sqlalchemy.orm import Session

from backend.domain.models.likes import Likes
from backend.domain.models.painting import Painting
from typing import Optional, List, Type

from backend.infrastructure.database.schemas.painting_schemas import PaintingPublic


class PaintingRepository:
    @staticmethod
    async def create_painting(
            artist_id: int,
            img_path: str,
            description: Optional[str] = None,
            db: Session = None
    ) -> PaintingPublic:
        new_painting = Painting(
            artist_id=artist_id,
            img_path=img_path,
            description=description
        )
        db.add(new_painting)
        db.commit()
        db.refresh(new_painting)
        return PaintingPublic.model_validate(new_painting)

    @staticmethod
    def get_painting_by_id(painting_id: int, db: Session) -> Optional[PaintingPublic]:
        painting = db.query(Painting).filter(Painting.id == painting_id).first()
        if not painting:
            return None
        return PaintingPublic.model_validate(painting)

    @staticmethod
    async def get_all_paintings(db: Session) -> List[PaintingPublic]:
        paintings = db.query(Painting).all()
        return [PaintingPublic.model_validate(painting) for painting in paintings]

    @staticmethod
    async def get_paintings_by_artist_id(artist_id: int, db: Session) -> List[PaintingPublic]:
        paintings = db.query(Painting).filter(Painting.artist_id == artist_id).all()
        return [PaintingPublic.model_validate(painting) for painting in paintings]

    @staticmethod
    async def update_painting_embedding(
            painting_id: int,
            img_embedding: List[float],
            db: Session
    ):
        painting = db.query(Painting).filter(Painting.id == painting_id).first()
        if not painting:
            return None

        painting.img_embedding = img_embedding
        db.commit()
        db.refresh(painting)
        return painting

    @staticmethod
    async def update_painting_tags(
            painting_id: int,
            img_tags: List[str],
            db: Session
    ):
        painting = db.query(Painting).filter(Painting.id == painting_id).first()
        if not painting:
            return None

        painting.img_tags = img_tags
        db.commit()
        db.refresh(painting)
        return painting

    @staticmethod
    async def add_likes_count(painting: Type[Painting], db: Session) -> Type[Painting]:
        if painting is not None:
            painting.count_likes = db.query(Likes).filter(Likes.painting_id == painting.id).count()
        return painting

    @staticmethod
    def get_artist_id_by_painting_id(painting_id: int, db: Session) -> Optional[int]:
        painting = db.query(Painting).filter(Painting.id == painting_id).first()
        if not painting:
            return None
        return painting.artist_id

    @staticmethod
    async def delete_painting(painting_id: int, db: Session) -> bool:
        painting = db.query(Painting).filter(Painting.id == painting_id).first()
        if painting:
            db.delete(painting)
            db.commit()
            return True
        return False

    @staticmethod
    async def update_painting(painting_id: int,
                              artist_id: int,
                              img_path: str,
                              description: str,
                              db: Session) -> Optional[PaintingPublic]:
        painting = db.query(Painting).filter(Painting.id == painting_id).first()
        if painting and painting.artist_id == artist_id:
            painting.img_path = img_path if img_path else painting.img_path
            painting.description = description if description else painting.description
            db.commit()
            db.refresh(painting)
            return PaintingPublic.model_validate(painting)
        return None

    @staticmethod
    def check_is_painting_img_path_exists(img_path: str, db: Session) -> bool:
        painting = db.query(Painting).filter(Painting.img_path == img_path).first()
        return True if painting else False
