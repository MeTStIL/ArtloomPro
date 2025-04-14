from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class AccountCreate(BaseModel):
    login: str
    password: str
    avatar_img_path: Optional[str] = None


class AccountLogin(BaseModel):
    login: str
    password: str

class AccountPublic(BaseSchema):
    id: int
    login: str
    avatar_img_path: Optional[str]
    artist_id: Optional[int]

class AccountFull(AccountPublic):
    hashed_password: str

class AccountUpdate(BaseSchema):
    login: Optional[str] = None
    avatar_img_path: Optional[str] = None

class AccountPublicWithLikesAndSubscribes(AccountPublic):
    subscribed_artist_ids: list[int]
    liked_paintings_ids: list[int]
    is_owner: bool

