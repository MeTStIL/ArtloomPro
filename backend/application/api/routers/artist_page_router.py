from fastapi import APIRouter, HTTPException
from backend.domain.models.artist_page import ArtistPage
from backend.infrastructure.database.repositories.artist_page_repository import ArtistPageRepository

router = APIRouter()


@router.get("/artist_pages/{artist_page_id}", response_model=ArtistPage)
async def get_artist_page(artist_page_id: int):
    artist_page_data = {
        "id": artist_page_id,
        "url": "https://artloom.ru/yuriromashov/",
        "artist_id": 1,
        "painting_ids": [1, 2, 3],
    }
    return ArtistPage(**artist_page_data)



@router.post("/artist_pages/")
async def create_artist_page(data: ArtistPage):
    artist_page = await ArtistPageRepository.create_artist_page(
        url=data.url,
        artist_id=data.artist_id,
        painting_ids=data.painting_ids
    )
    return {"id": artist_page.id, "url": artist_page.url, "artist_id": artist_page.artist_id}
