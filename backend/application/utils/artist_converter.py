from sqlalchemy.orm import Session

from backend.infrastructure.database.repositories.artist_page_repository import \
    ArtistPageRepository
from backend.infrastructure.database.repositories.subscribes_repository import \
    SubscribesRepository
from backend.infrastructure.database.schemas.artist_schemas import ArtistPublic, \
    ArtistPublicWithSubsCountAndArtistPageId


def add_to_artist_subs_count_and_artist_page_id(artist_public: ArtistPublic, db: Session) -> ArtistPublicWithSubsCountAndArtistPageId:
    return ArtistPublicWithSubsCountAndArtistPageId(
        id=artist_public.id,
        name=artist_public.name,
        description=artist_public.description,
        img_path=artist_public.img_path,
        subscribers_count=SubscribesRepository.get_subscribers_count(artist_public.id, db),
        artist_page_id=ArtistPageRepository.get_artist_page_by_artist_id(artist_public.id, db).id
    )
