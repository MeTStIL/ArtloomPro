from fastapi import APIRouter, HTTPException
from typing import List

from backend.domain.models.artist import Artist
from backend.infrastructure.database.repositories.artist_repository import ArtistRepository

router = APIRouter()


@router.get("/artists/", response_model=List[Artist])
async def get_artists():
    artists = await ArtistRepository.get_all_artists()
    return artists


@router.get("/artists/{artist_id}", response_model=Artist)
async def get_artist_by_id(artist_id: int):
    artist_data = {
        "id": artist_id,
        "name": "Yuri Romashov",
        "img_url": "https://filin.mail.ru/pic?d=W-4HTBnEGVHZQyhxKlUYEadnaFQIYUwliSIoopmNw4JMOa86FN7GIQMY1N8ybWeyIhn6RU1v&width=240&height=240&quo",
        "contacts": "telegram: @yurec121",
        "description": "Yuri Romashov is an amazingly talented artist from "
                       "Russia. He creates in the genre of digital art",
    }
    return Artist(**artist_data)


@router.post("/artists/", response_model=Artist)
async def create_artist(artist: Artist):
    new_artist = await ArtistRepository.create_artist(
        name=artist.name,
        img_url=artist.img_url,
        contacts=artist.contacts,
        description=artist.description
    )
    return new_artist
