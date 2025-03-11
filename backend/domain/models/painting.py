from pydantic import BaseModel, Field
from typing import Optional
from tortoise import fields
from tortoise.models import Model


class Painting(BaseModel):
    id: int = Field(..., description='ID Картины', example=1)
    title: str = Field(..., description='Название картины', example='Апофеоз войны')
    artist_account_id: int = Field(..., description='ID профиля Художника', example=1)
    img_url: str = Field(..., description='Ссылка на картину', example='https://www.example.com/paintings/sample.jpg')
    year: Optional[int] = Field(None, description='Год написания картины', example=1871)
    description: Optional[str] = Field(None, description='Описание картины', example='Посвящается всем великим завоевателям — прошедшим, настоящим и будущим')
    medium: Optional[str] = Field(None, description='Основные характеристики картины', example='Холст, Масло. 127 × 197 см')
    times_favorite: Optional[int] = None


class PaintingDB(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    artist_account = fields.ForeignKeyField("models.ArtistDB", related_name="paintings",
                                            on_delete=fields.CASCADE)
    img_url = fields.CharField(max_length=255)
    year = fields.IntField(null=True)
    description = fields.TextField(null=True)
    medium = fields.CharField(max_length=100, null=True)

    class Meta:
        table = "paintings"
