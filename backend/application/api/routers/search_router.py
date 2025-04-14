from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.schemas.search_schemas import *
from backend.domain.logic.text_embedding import get_text_embedding
from backend.infrastructure.database.repositories.search_repository import SearchRepository

router = APIRouter()

@router.post("/search-paintings/", response_model=list[int])
async def search_paintings(
        search_query: SearchQuery,
        db: Session = Depends(get_db)
):
    text_embedding = get_text_embedding(search_query.text)

    search_result = SearchRepository.search_painting_ids(
        text_embedding,
        search_query.limit, db
    )

    return search_result

@router.post("/random-paintings/", response_model=list[int])
async def random_paintings(
        search_query: RandomSearchQuery,
        db: Session = Depends(get_db)
):
    result = SearchRepository.get_random_painting_ids(search_query.limit, db)
    return result