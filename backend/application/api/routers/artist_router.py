from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from backend.domain.logic.photo_uploader import upload_photo_to_yc
from backend.application.auth.handler import get_current_account_by_login
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.account_repository import AccountRepository
from backend.infrastructure.database.repositories.artist_page_repository import ArtistPageRepository
from backend.infrastructure.database.repositories.artist_repository import ArtistRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull
from backend.infrastructure.database.schemas.artist_schemas import ArtistPublic, ArtistCreate, ArtistUpdate, ArtistPublicWithSubsCountAndArtistPageId
from backend.application.utils.artist_converter import add_to_artist_subs_count_and_artist_page_id

router = APIRouter(prefix="/artists")


@router.get("/{artist_id}", response_model=ArtistPublicWithSubsCountAndArtistPageId)
async def get_artist_by_id(artist_id: int, db: Session = Depends(get_db)):
    artist = ArtistRepository.get_artist_by_id(artist_id, db)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    print(1)
    return add_to_artist_subs_count_and_artist_page_id(artist, db)


@router.post("/", response_model=ArtistPublicWithSubsCountAndArtistPageId)
async def create_artist(artist: ArtistCreate, db: Session = Depends(get_db),
                        current_account: AccountFull = Depends(get_current_account_by_login)):
    if ArtistRepository.get_artist_by_account_id(current_account.id, db):
        raise HTTPException(status_code=403, detail="You already have an artist")
    artist = ArtistRepository.create_artist(artist, db)
    ArtistPageRepository.create_artist_page(artist.id, db)

    AccountRepository.add_artist_to_account(artist.id, current_account.id, db)

    return add_to_artist_subs_count_and_artist_page_id(artist, db)

@router.delete("/")
async def delete_artist(db: Session = Depends(get_db),
                        current_account: AccountFull = Depends(get_current_account_by_login)):
    artist_id = current_account.artist_id
    artist = ArtistRepository.delete_artist(artist_id, db)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "Artist deleted successfully"}

@router.patch("/", response_model=ArtistPublicWithSubsCountAndArtistPageId)
async def update_artist(new_artist: ArtistUpdate, db: Session = Depends(get_db),
                        current_account: AccountFull = Depends(get_current_account_by_login)):
    artist_id = current_account.artist_id
    if artist_id is None:
        raise HTTPException(status_code=403, detail="You don't have an artist")
    new_artist_dict = new_artist.model_dump(exclude_unset=True)
    artist = ArtistRepository.update_artist(artist_id, new_artist_dict, db)
    return add_to_artist_subs_count_and_artist_page_id(artist, db)

@router.get("/", response_model=ArtistPublicWithSubsCountAndArtistPageId)
def get_current_user_artist(db: Session = Depends(get_db),
                            current_account: AccountFull = Depends(get_current_account_by_login)):
    artist = ArtistRepository.get_artist_by_account_id(current_account.id, db)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    return add_to_artist_subs_count_and_artist_page_id(artist, db)
