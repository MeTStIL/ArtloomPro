from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.application.auth.handler import get_current_account_by_login, \
    get_current_account_or_none
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.schemas.account_schemas import (AccountPublic, AccountFull, AccountUpdate,
                                                                     AccountPublicWithLikesAndSubscribes)
from backend.application.utils.account_converter import add_to_account_likes_and_subs

router = APIRouter(prefix="/accounts")


@router.get("/{login}", response_model=AccountPublicWithLikesAndSubscribes)
def get_account(login: str, db: Session = Depends(get_db),
                user: AccountFull = Depends(get_current_account_or_none)):
    account = AccountRepository.get_account_info_by_login(login, db)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return add_to_account_likes_and_subs(account, user, db)

@router.patch("/", response_model=AccountPublicWithLikesAndSubscribes)
def update_account(account: AccountUpdate, db: Session = Depends(get_db),
                   user: AccountFull = Depends(get_current_account_by_login)):
    if account.login and not AccountRepository.is_login_unique(account.login, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    account_dict = account.model_dump(exclude_unset=True)
    account = AccountRepository.update_account(user.id, account_dict, db)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    return add_to_account_likes_and_subs(account, user, db)


@router.delete("/")
def delete_account(db: Session = Depends(get_db),
                   user: AccountFull = Depends(get_current_account_by_login)):
    deleted = AccountRepository.delete_account(user.id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return {"message": "Account deleted"}

@router.get("/", response_model=AccountPublicWithLikesAndSubscribes)
def get_my_account(db: Session = Depends(get_db),
                   user: AccountFull = Depends(get_current_account_by_login)):
    account = AccountRepository.get_account_info_by_login(user.login, db)
    return add_to_account_likes_and_subs(account, user, db)
