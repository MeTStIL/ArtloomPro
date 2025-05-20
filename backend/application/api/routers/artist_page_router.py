from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.application.auth.handler import get_current_account_by_login, \
    get_current_account_or_none
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.artist_page_repository import ArtistPageRepository
from backend.infrastructure.database.repositories.artist_repository import ArtistRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull
from backend.infrastructure.database.schemas.artist_page_schemas import (ArtistPagePublic,
                                                                         ArtistPagePublicWithPaintingsIdsAndUrl)
from backend.application.utils.artist_page_converter import add_to_artist_page_painting_ids_and_url

router = APIRouter()


@router.get("/artist-pages/{id}", response_model=ArtistPagePublicWithPaintingsIdsAndUrl)
async def get_artist_page(id: int, db: Session = Depends(get_db),
                user: AccountFull = Depends(get_current_account_or_none)):
    artist_page = ArtistPageRepository.get_artist_page_by_id(id, db)
    if artist_page is None:
        raise HTTPException(status_code=404, detail="ArtistPage not found")

    artist_page = ArtistPagePublic.model_validate(artist_page)
    return add_to_artist_page_painting_ids_and_url(artist_page, user, db)

@router.get("/artist-pages/by_login/{login}", response_model=ArtistPagePublicWithPaintingsIdsAndUrl)
async def get_artist_page(login: str, db: Session = Depends(get_db),
                user: AccountFull = Depends(get_current_account_or_none)):
    artist_page = ArtistPageRepository.get_artist_page_by_login(login, db)
    if artist_page is None:
        raise HTTPException(status_code=404, detail="ArtistPage not found")

    artist_page = ArtistPagePublic.model_validate(artist_page)
    return add_to_artist_page_painting_ids_and_url(artist_page, user, db)

@router.delete("/artist_pages/")
async def delete_artist_page(db: Session = Depends(get_db),
                             user: AccountFull = Depends(get_current_account_by_login)):

    """Тут теперь удаление не artist_page, а самого artist. При удалении страницы каскадно не будет ставиться id в null,
    это связано с реализацией самой алхимии. При удалении артиста всё норм, могу потом подробнее расписать"""
    deleted = ArtistRepository.delete_artist(user.artist_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "ArtistPage deleted"}

