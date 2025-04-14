from typing import Optional
from sqlalchemy.orm import Session
from backend.domain.models.account import Account
from sqlalchemy.exc import IntegrityError

from backend.domain.models.artist_page import ArtistPage
from backend.infrastructure.database.schemas.account_schemas import AccountFull, AccountPublic
from backend.domain.models.likes import Likes
from backend.domain.models.subscribes import Subscribes
from backend.infrastructure.database.schemas.account_schemas import AccountFull


class AccountRepository:
    @staticmethod
    def create_account(login: str,
                       hashed_password: str,
                       avatar_img_path: Optional[str],
                       db: Session) -> Optional[AccountPublic]:
        try:
            account = Account(
                login=login,
                hashed_password=hashed_password,
                avatar_img_path=avatar_img_path,
            )
            db.add(account)
            db.commit()
            db.refresh(account)
            return AccountPublic.model_validate(account)
        except IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def get_account_full_info_by_login(login: str, db: Session) -> Optional[AccountFull]:
        account = db.query(Account).filter_by(login=login).first()
        if not account:
            return None
        return AccountFull.model_validate(account)

    @staticmethod
    async def set_like(login: str, painting_id: int, db: Session):
        account_id = db.query(Account).filter_by(login=login).first().id

        existing_like = db.query(Likes).filter(
            Likes.account_id == account_id,
            Likes.painting_id == painting_id
        ).first()

        if existing_like:
            raise ValueError

        new_like = Likes(
            account_id=account_id,
            painting_id=painting_id
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)

    @staticmethod
    async def delete_like(login: str, painting_id: int, db: Session):
        account_id = db.query(Account).filter_by(login=login).first().id

        existing_like = db.query(Likes).filter(
            Likes.account_id == account_id,
            Likes.painting_id == painting_id
        ).first()
        if not existing_like:
            raise ValueError

        db.delete(existing_like)
        db.commit()

    @staticmethod
    def get_account_info_by_login(login: str, db: Session) -> Optional[AccountPublic]:
        account = db.query(Account).filter_by(login=login).first()
        if account:
            return AccountPublic.model_validate(account)
        return None

    @staticmethod
    def delete_account(id: int, db: Session) -> bool:
        account = db.query(Account).filter_by(id=id).first()
        if account:
            db.delete(account)
            db.commit()
            return True
        return False

    @staticmethod
    def update_account(id: int, update_data: dict, db: Session) -> Optional[AccountPublic]:
        account = db.query(Account).filter_by(id=id).first()
        if not account:
            return None

        for key, value in update_data.items():
            setattr(account, key, value)

        db.commit()
        db.refresh(account)
        return AccountPublic.model_validate(account)

    @staticmethod
    def is_login_unique(login: str, db: Session) -> bool:
        return not db.query(Account).filter_by(login=login).first()

    @staticmethod
    def add_artist_to_account(artist_id: int, account_id: int, db: Session) -> bool:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            account.artist_id = artist_id
            db.commit()
            return True
        return False

    @staticmethod
    async def subscribe(login: str, artist_id: int, db: Session):
        account_id = db.query(Account).filter_by(login=login).first().id

        existing_subscribe = db.query(Subscribes).filter(
            Subscribes.account_id == account_id,
            Subscribes.artist_id == artist_id
        ).first()

        if existing_subscribe:
            raise ValueError

        new_subscribe = Subscribes(
            account_id=account_id,
            artist_id=artist_id
        )
        db.add(new_subscribe)
        db.commit()
        db.refresh(new_subscribe)

    @staticmethod
    async def unsubscribe(login: str, artist_id: int, db: Session):
        account_id = db.query(Account).filter_by(login=login).first().id

        existing_subscribe = db.query(Subscribes).filter(
            Subscribes.account_id == account_id,
            Subscribes.artist_id == artist_id
        ).first()
        if not existing_subscribe:
            raise ValueError

        db.delete(existing_subscribe)
        db.commit()

    @staticmethod
    def get_account_by_artist_page_id(artist_page_id: int, db: Session) -> Optional[AccountPublic]:
        artist_page = db.query(ArtistPage).filter_by(id=artist_page_id).first()
        if not artist_page:
            return None

        account = db.query(Account).filter_by(artist_id=artist_page.artist_id).first()
        print(AccountPublic.model_validate(account).login)

        return AccountPublic.model_validate(account) if account else None
