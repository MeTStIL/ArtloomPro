from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, BackgroundTasks, status
from typing import List
from sqlalchemy.orm import Session

from backend.application.auth.handler import get_current_account_by_login
from backend.domain.logic.photo_uploader import upload_photo_to_yc, delete_photo_from_yc
from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.painting_repository import PaintingRepository
from backend.infrastructure.database.schemas.account_schemas import AccountFull
from backend.infrastructure.database.schemas.painting_schemas import (PaintingPublic, PaintingCreate, PaintingUpdate,
                                                                      PaintingPublicWithLikesCount)
from backend.application.services.embedding_service import generate_and_save_embedding
from backend.application.services.tags_service import generate_and_save_tags
from backend.application.utils.painting_converter import add_to_painting_likes_count

router = APIRouter(prefix="/paintings")


@router.get("/", response_model=List[PaintingPublicWithLikesCount])
async def get_paintings(db: Session = Depends(get_db)):
    paintings = await PaintingRepository.get_all_paintings(db)
    return [add_to_painting_likes_count(painting, db) for painting in paintings]


@router.get("/{painting_id}", response_model=PaintingPublicWithLikesCount)
async def get_painting_by_id(painting_id: int, db: Session = Depends(get_db)):
    painting = PaintingRepository.get_painting_by_id(painting_id, db)
    if painting is None:
        raise HTTPException(status_code=404, detail="Painting not found")

    return add_to_painting_likes_count(painting, db)

@router.post("/", response_model=PaintingPublicWithLikesCount)
async def create_painting(painting: PaintingCreate,
                          background_tasks: BackgroundTasks,
                          db: Session = Depends(get_db),
                          current_account: AccountFull = Depends(get_current_account_by_login)):
    artist_id = current_account.artist_id

    if PaintingRepository.check_is_painting_img_path_exists(painting.img_path, db):
        raise HTTPException(status_code=400, detail="Painting with this image already exists")

    new_painting = await PaintingRepository.create_painting(
        artist_id=artist_id,
        img_path=painting.img_path,
        description=painting.description,
        db=db
    )

    background_functions = [generate_and_save_embedding, generate_and_save_tags]
    for func in background_functions:
        background_tasks.add_task(
            func,
            painting_id=new_painting.id,
            img_path=new_painting.img_path
        )
    return add_to_painting_likes_count(new_painting, db)


@router.patch("/{painting_id}", response_model=PaintingPublicWithLikesCount)
async def update_painting(painting_id: int, painting_new: PaintingUpdate, db: Session = Depends(get_db),
                          current_account: AccountFull = Depends(get_current_account_by_login)):
    painting = PaintingRepository.get_painting_by_id(painting_id, db)
    if painting is None:
        raise HTTPException(status_code=404, detail="Painting not found")
    # if painting_new.img_path and PaintingRepository.check_is_painting_img_path_exists(painting_new.img_path, db):
    #     raise HTTPException(status_code=400, detail="Painting with this image already exists")
    if painting.artist_id != current_account.artist_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to update this painting")

    updated_painting = await PaintingRepository.update_painting(
        painting_id=painting_id,
        artist_id=current_account.artist_id,
        description=painting_new.description if painting_new.description else painting.description,
        db=db,
        img_path=painting_new.img_path if painting_new.img_path else painting.img_path
    )
    if not updated_painting:
        raise HTTPException(status_code=404, detail="Painting not found")

    return add_to_painting_likes_count(updated_painting, db)


@router.delete("/{painting_id}")
async def delete_painting(painting_id: int, db: Session = Depends(get_db),
                          current_account: AccountFull = Depends(get_current_account_by_login)):
    painting = PaintingRepository.get_painting_by_id(painting_id, db)
    if painting is None:
        raise HTTPException(status_code=404, detail="Painting not found")
    if painting.artist_id != current_account.artist_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to delete this account")

    await PaintingRepository.delete_painting(painting_id, db)
    delete_photo_from_yc(painting.img_path)
    return {"message": "Painting deleted successfully"}
