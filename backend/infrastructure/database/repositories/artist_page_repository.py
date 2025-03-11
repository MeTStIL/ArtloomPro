from typing import Optional, List

from backend.domain.models.artist_page import ArtistPageDB
from backend.domain.models.painting import PaintingDB
from tortoise.transactions import in_transaction


class ArtistPageRepository:
    @staticmethod
    async def create_artist_page(url: str, artist_id: int, painting_ids: Optional[List[int]] = None):
        async with in_transaction():
            artist_page = await ArtistPageDB.create(url=url, artist_id=artist_id)

            if painting_ids:
                paintings = await PaintingDB.filter(id__in=painting_ids)
                await artist_page.paintings.add(*paintings)

            return artist_page

    @staticmethod
    async def get_artist_page_by_id(artist_page_id: int):
        artist_page = await ArtistPageDB.get_or_none(id=artist_page_id).prefetch_related("paintings")

        if not artist_page:
            return None

        return {
            "url": artist_page.url,
            "artist_id": artist_page.artist_id,
            "painting_ids": [painting.id for painting in artist_page.paintings]
        }
