from pydantic import BaseModel, Field
from typing import Optional, List
from tortoise.models import Model
from tortoise import fields


class Account(BaseModel):
    id: int
    login: str
    avatar_img_url: Optional[str] = None
    favourite_painting_ids: Optional[List[int]] = None
    subscribed_artist_ids: Optional[List[int]] = None
