from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.application.auth.handler import get_current_account_by_login
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.repositories.painting_repository import PaintingRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull

router = APIRouter()

@router.post("/set_like/{painting_id}")
async def set_like(painting_id: int, db: Session = Depends(get_db),
                   user: AccountFull = Depends(get_current_account_by_login)):
    try:
        if not PaintingRepository.get_painting_by_id(painting_id, db):
            raise HTTPException(status_code=404, detail="Painting not found")
        await AccountRepository.set_like(user.login, painting_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="This account has already liked this painting")

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Like successfully set",
            "data": {
                "account_login": user.login,
                "painting_id": painting_id
            }
        }
    )

@router.delete("/delete_like/{painting_id}")
async def delete_like(painting_id: int, db: Session = Depends(get_db), user: AccountFull = Depends(get_current_account_by_login)):
    try:
        if not PaintingRepository.get_painting_by_id(painting_id, db):
            raise HTTPException(status_code=404, detail="Painting not found")
        await AccountRepository.delete_like(user.login, painting_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="This account has not liked this painting yet")

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Like successfully deleted",
            "data": {
                "account_login": user.login,
                "painting_id": painting_id
            }
        }
    )