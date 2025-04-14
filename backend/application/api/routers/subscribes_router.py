from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.application.auth.handler import get_current_account_by_login
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.repositories.artist_repository import ArtistRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull

router = APIRouter()

@router.post("/subscribe/{artist_id}")
async def subscribe(artist_id: int, db: Session = Depends(get_db),
                    user: AccountFull = Depends(get_current_account_by_login)):
    if not ArtistRepository.get_artist_by_id(artist_id, db):
        raise HTTPException(status_code=404, detail="Artist not found")
    try:
        await AccountRepository.subscribe(user.login, artist_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="This account is already subscribed to this artist")

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Subscribe was successful",
            "data": {
                "account_login": user.login,
                "artist_id": artist_id
            }
        }
    )

@router.delete("/unsubscribe/{artist_id}")
async def unsubscribe(artist_id: int, db: Session = Depends(get_db),
                      user: AccountFull = Depends(get_current_account_by_login)):
    if not ArtistRepository.get_artist_by_id(artist_id, db):
        raise HTTPException(status_code=404, detail="Artist not found")
    try:
        await AccountRepository.unsubscribe(user.login, artist_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="This account is not subscribed to this artist")

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Unsubscribe was successful",
            "data": {
                "account_login": user.login,
                "artist_id": artist_id
            }
        }
    )
