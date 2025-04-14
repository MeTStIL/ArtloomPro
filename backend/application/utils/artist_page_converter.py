from sqlalchemy.orm import Session

from backend.infrastructure.database.repositories.artist_page_repository import ArtistPageRepository
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull
from backend.infrastructure.database.schemas.artist_page_schemas import ArtistPagePublic, ArtistPagePublicWithPaintingsIdsAndUrl


def add_to_artist_page_painting_ids_and_url(artist_page: ArtistPagePublic, user: AccountFull, db: Session) -> ArtistPagePublicWithPaintingsIdsAndUrl:
    return ArtistPagePublicWithPaintingsIdsAndUrl(
        id=artist_page.id,
        url=ArtistPageRepository.get_url_by_artist_id(artist_page.artist_id, db),
        artist_id=artist_page.artist_id,
        painting_ids=ArtistPageRepository.get_painting_ids(artist_page.artist_id, db),
        is_owner=(False if user is None else AccountRepository.get_account_by_artist_page_id(artist_page.id, db).id == user.id),
    )
