from pydantic import BaseModel, Field
from typing import Optional
from tortoise.models import Model
from tortoise import fields


class Artist(BaseModel):
    id: int = Field(..., description='ID Художника', example=1)
    name: str = Field(..., description='Имя Художника', example='Василий Васильевич Верещагин')
    img_url: Optional[str] = Field(None, description='Аватар Художника', example='https://www.example.com/images/sample.jpg')
    contacts: Optional[str] = Field(None, description='Контактная информация Художника', example='Telegram: @VasilyVereshchagin')
    description: Optional[str] = Field(None, description='Информация о Художнике', example='Русский живописец, писатель, один из самых известных баталистов второй половины XIX века.')
    subscribers_count: Optional[int] = None


class ArtistDB(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    img_url = fields.CharField(max_length=255, null=True)
    contacts = fields.TextField(null=True)
    description = fields.TextField(null=True)

    class Meta:
        table = "artists"
