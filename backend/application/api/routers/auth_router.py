from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.application.auth.hash import verify_password
from backend.application.auth.tokens import create_access_token
from backend.domain.models.account import Token
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull
from backend.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/auth/", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = AccountRepository.get_account_full_info_by_login(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = AccountFull.model_validate(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.login)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
