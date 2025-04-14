from typing import Optional
from pydantic import BaseModel

class SearchQuery(BaseModel):
    text: str
    limit: int

class RandomSearchQuery(BaseModel):
    limit: int

class PaintingSearchResult(BaseModel):
    id: int
    score: float
