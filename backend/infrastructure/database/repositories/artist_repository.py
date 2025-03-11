from typing import Optional

from backend.domain.models.artist import ArtistDB


class ArtistRepository:
    @staticmethod
    async def create_artist(name: str, img_url: Optional[str] = None, contacts: Optional[str] = None,
                            description: Optional[str] = None):
        return await ArtistDB.create(
            name=name,
            img_url=img_url,
            contacts=contacts,
            description=description
        )

    @staticmethod
    async def get_artist_by_id(artist_id: int):
        return await ArtistDB.filter(id=artist_id).first()
