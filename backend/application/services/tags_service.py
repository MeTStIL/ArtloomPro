import asyncio
from typing import List
from sqlalchemy.orm import Session

from backend.infrastructure.database.config import get_db
from backend.infrastructure.database.repositories.painting_repository import PaintingRepository
from backend.domain.logic.image_tags import get_image_tags


async def generate_and_save_tags(painting_id: int, img_path: str):
    db: Session = next(get_db())
    try:
        loop = asyncio.get_event_loop()
        tags: List[str] = await loop.run_in_executor(
            None,
            get_image_tags,
            img_path
        )

        if tags:
            await PaintingRepository.update_painting_tags(
                painting_id=painting_id,
                img_tags=tags,
                db=db
            )
    except Exception as e:
        print(f"Error in generate_and_save_tags: {e}")
    finally:
        db.close()
