from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.application.auth.hash import hash_password
from backend.application.auth.tokens import create_access_token
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.schemas.account_schemas import AccountPublicWithLikesAndSubscribes, AccountCreate
from backend.domain.models.account import Token
from backend.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register/", response_model=Token)
def register_user(user: AccountCreate, db: Session = Depends(get_db)) -> Token:
    if not AccountRepository.is_login_unique(user.login, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_password = hash_password(user.password)
    account = AccountRepository.create_account(user.login, hashed_password, user.avatar_img_path, db)
    if not account:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create account")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.login)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
