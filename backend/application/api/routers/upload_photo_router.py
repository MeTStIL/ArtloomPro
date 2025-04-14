from fastapi import APIRouter, UploadFile, File

from backend.domain.logic.photo_uploader import upload_photo_to_yc

router = APIRouter()


@router.post("/upload-photo/")
async def upload_photo(file: UploadFile = File(...)):
    return upload_photo_to_yc(file)
