import asyncio
from typing import List
from sqlalchemy.orm import Session

from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.painting_repository import PaintingRepository
from backend.domain.logic.image_embedding import get_image_embedding

async def generate_and_save_embedding(painting_id: int, img_path: str):
    db: Session = next(get_db())
    try:
        loop = asyncio.get_event_loop()
        img_embedding: List[float] = await loop.run_in_executor(
            None,
            get_image_embedding,
            img_path
        )

        if img_embedding:
            await PaintingRepository.update_painting_embedding(
                painting_id=painting_id,
                img_embedding=img_embedding,
                db=db
            )
    except Exception as e:
        print(f"Error in generate_and_save_embedding: {e}")
    finally:
        db.close()
