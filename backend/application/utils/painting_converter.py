from sqlalchemy.orm import Session

from backend.infrastructure.database.repositories.artist_page_repository import \
    ArtistPageRepository
from backend.infrastructure.database.repositories.likes_repository import LikesRepository
from backend.infrastructure.database.schemas.painting_schemas import PaintingPublic, PaintingPublicWithLikesCount


def add_to_painting_likes_count(painting: PaintingPublic, db: Session) -> PaintingPublicWithLikesCount:
    return PaintingPublicWithLikesCount(
        id=painting.id,
        artist_id=painting.artist_id,
        img_path=painting.img_path,
        description=painting.description,
        likes_count=LikesRepository.get_likes_count(painting.id, db),
        artist_page_url=ArtistPageRepository.get_url_by_artist_id(painting.artist_id, db)
    )
