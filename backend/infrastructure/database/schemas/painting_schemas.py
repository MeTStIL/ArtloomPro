from typing import Optional

from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class PaintingCreate(BaseSchema):
    img_path: str
    description: Optional[str] = None

class PaintingPublic(PaintingCreate):
    id: int
    artist_id: int

class PaintingPublicWithLikesCount(PaintingPublic):
    likes_count: int

class PaintingUpdate(BaseSchema):
    description: Optional[str] = None
    img_path: Optional[str] = None
