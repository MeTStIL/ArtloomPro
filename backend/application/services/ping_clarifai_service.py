import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.domain.logic.text_embedding import get_text_embedding
from time import time

async def ping_clarifai_model():
    while True:
        get_text_embedding(str(time()))
        await asyncio.sleep(240)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(ping_clarifai_model())
    yield