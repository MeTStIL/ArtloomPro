from typing import Optional, List

from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class ArtistPageCreate(BaseSchema):
    artist_id: int

class ArtistPagePublic(ArtistPageCreate):
    id: int


class ArtistPagePublicWithPaintingsIdsAndUrl(ArtistPagePublic):
    painting_ids: Optional[List[int]]
    url: str
    is_owner: bool
