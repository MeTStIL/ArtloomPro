from sqlalchemy.orm import Session

from backend.infrastructure.database.schemas.account_schemas import AccountPublicWithLikesAndSubscribes, \
    AccountPublic, AccountFull
from backend.infrastructure.database.repositories.likes_repository import LikesRepository
from backend.infrastructure.database.repositories.subscribes_repository import SubscribesRepository


def add_to_account_likes_and_subs(account_public: AccountPublic, user: AccountPublic, db: Session) -> AccountPublicWithLikesAndSubscribes:
    return AccountPublicWithLikesAndSubscribes(
        id=account_public.id,
        login=account_public.login,
        avatar_img_path=account_public.avatar_img_path,
        artist_id=account_public.artist_id,
        subscribed_artist_ids=SubscribesRepository.get_subscribed_artist_ids(account_public.id, db),
        liked_paintings_ids=LikesRepository.get_liked_painting_ids(account_public.id, db),
        is_owner=(False if user is None else account_public.id == user.id)
    )
