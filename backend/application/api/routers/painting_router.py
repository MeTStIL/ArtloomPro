from fastapi import APIRouter, HTTPException
from typing import List

from backend.domain.models.painting import Painting
from backend.infrastructure.database.repositories.painting_repository import PaintingRepository

router = APIRouter()


@router.get("/paintings/", response_model=List[Painting])
async def get_paintings():
    paintings = await PaintingRepository.get_all_paintings()
    return paintings


@router.get("/paintings/{painting_id}", response_model=Painting)
async def get_painting_by_id(painting_id: int):
    painting_data = {
        "id": painting_id,
        "title": "Yura's sad story",
        "artist_account_id": 1,
        "img_url": "https://upload.wikimedia.org/wikipedia/ru/9/9c/George_Floyd.png",
        "year": 2024,
        "description": "A story of unrequited love and fear of confessing your"
                       " feelings to a girl",
        "medium": "Digital art"
    }
    return Painting(**painting_data)


@router.post("/paintings/", response_model=Painting)
async def create_painting(painting: Painting):
    new_painting = await PaintingRepository.create_painting(
        title=painting.title,
        artist_account_id=painting.artist_account_id,
        img_url=painting.img_url,
        year=painting.year,
        description=painting.description,
        medium=painting.medium
    )
    return new_painting
