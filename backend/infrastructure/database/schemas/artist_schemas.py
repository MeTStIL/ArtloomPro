from typing import Optional

from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class ArtistCreate(BaseSchema):
    name: str
    img_path: Optional[str] = None
    description: Optional[str] = None

class ArtistPublic(ArtistCreate):
    id: int

class ArtistPublicWithSubsCountAndArtistPageUrl(ArtistPublic):
    subscribers_count: int
    artist_page_url: str

class ArtistUpdate(BaseSchema):
    name: Optional[str] = None
    img_path: Optional[str] = None
    description: Optional[str] = None
