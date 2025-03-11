import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.infrastructure.database.config import init_db
from backend.application.api.routers import painting_router
from backend.application.api.routers import artist_router
from backend.application.api.routers import artist_page_router
from backend.application.api.routers import account_router

app = FastAPI()

#init_db(app)

app.include_router(painting_router.router)
app.include_router(artist_router.router)
app.include_router(artist_page_router.router)
app.include_router(account_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.get("/")
async def home():
    return {"message": "Добро пожаловать в Artloom!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
