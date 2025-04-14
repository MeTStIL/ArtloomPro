from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.infrastructure.database.repositories.account_repository import AccountRepository

from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.schemas.account_schemas import AccountFull
from backend.settings import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

def get_current_account_by_login(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> AccountFull:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_login: str = payload.get("sub")

        if user_login is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = AccountRepository.get_account_full_info_by_login(user_login, db)
    if user is None:
        raise credentials_exception

    return AccountFull.model_validate(user)

def get_current_account_or_none(token: str = Depends(oauth2_scheme),
                                db: Session = Depends(get_db)) -> Optional[AccountFull]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_login: str = payload.get("sub")

        if user_login is None:
            return None

    except JWTError:
        return None

    user = AccountRepository.get_account_full_info_by_login(user_login, db)
    if user is None:
        return None

    return AccountFull.model_validate(user)
