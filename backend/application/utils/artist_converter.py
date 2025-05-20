from sqlalchemy.orm import Session

from backend.infrastructure.database.repositories.artist_page_repository import \
    ArtistPageRepository
from backend.infrastructure.database.repositories.subscribes_repository import \
    SubscribesRepository
from backend.infrastructure.database.schemas.artist_schemas import ArtistPublic, \
    ArtistPublicWithSubsCountAndArtistPageUrl


def add_to_artist_subs_count_and_artist_page_url(artist_public: ArtistPublic, db: Session) -> ArtistPublicWithSubsCountAndArtistPageUrl:
    return ArtistPublicWithSubsCountAndArtistPageUrl(
        id=artist_public.id,
        name=artist_public.name,
        description=artist_public.description,
        img_path=artist_public.img_path,
        artist_page_url=ArtistPageRepository.get_url_by_artist_id(artist_public.id, db),
        subscribers_count=SubscribesRepository.get_subscribers_count(artist_public.id, db),
    )
