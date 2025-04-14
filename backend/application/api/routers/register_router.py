from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.application.auth.hash import hash_password
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.schemas.account_schemas import AccountPublicWithLikesAndSubscribes, AccountCreate
from backend.application.utils.account_converter import add_to_account_likes_and_subs

router = APIRouter()

@router.post("/register", response_model=AccountPublicWithLikesAndSubscribes)
def register_user(user: AccountCreate, db: Session = Depends(get_db)) -> AccountPublicWithLikesAndSubscribes:
    if not AccountRepository.is_login_unique(user.login, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_password = hash_password(user.password)
    account = AccountRepository.create_account(user.login, hashed_password, user.avatar_img_path, db)
    if not account:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create account")

    return add_to_account_likes_and_subs(account, account, db)
