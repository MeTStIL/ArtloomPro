from backend.domain.models.painting import PaintingDB
from typing import Optional


class PaintingRepository:
    @staticmethod
    async def create_painting(
            title: str,
            artist_account_id: int,
            img_url: str,
            year: Optional[int] = None,
            description: Optional[str] = None,
            medium: Optional[str] = None
    ):
        return await PaintingDB.create(
            title=title,
            artist_account_id=artist_account_id,
            img_url=img_url,
            year=year,
            description=description,
            medium=medium
        )

    @staticmethod
    async def get_painting_by_id(painting_id: int):
        return await PaintingDB.filter(id=painting_id).first()
