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
    search_result_by_desc = SearchRepository.search_painting_ids_by_description(search_query.text,
                                                                                search_query.limit // 2,
                                                                                db)
    search_result_by_img = SearchRepository.search_painting_ids_by_image(
        text_embedding,
        search_query.limit,
        db
    )

    for painting_id in search_result_by_img:
        if painting_id in search_result_by_desc:
            continue
        search_result_by_desc.append(painting_id)
        if len(search_result_by_desc) == search_query.limit:
            break

    return search_result_by_desc

@router.post("/random-paintings/", response_model=list[int])
async def random_paintings(
        search_query: RandomSearchQuery,
        db: Session = Depends(get_db)
):
    result = SearchRepository.get_random_painting_ids(search_query.limit, db)
    return result
