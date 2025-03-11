from pydantic import BaseModel, Field
from typing import Optional, List
from tortoise.models import Model
from tortoise import fields


class ArtistPage(BaseModel):
    id: int = Field(..., description='ID личной страницы Художника', example=1)
    url: str = Field(..., description='Ссылка на личную страницу Художника', example='https://www.example.com/pages/VasilyVereshchagin')
    artist_id: int = Field(..., description='ID Художника', example=1)
    painting_ids: Optional[list[int]] = Field(..., description='Список ID картин Художника', example=[1,2,3])


class ArtistPageDB(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, unique=True)
    artist = fields.ForeignKeyField("models.ArtistDB", related_name="pages", on_delete=fields.CASCADE)
    paintings = fields.ManyToManyField("models.PaintingDB", related_name="artist_pages")

    class Meta:
        table = "artist_pages"
