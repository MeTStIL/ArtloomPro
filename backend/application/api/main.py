import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.application.api.routers import painting_router
from backend.application.api.routers import artist_router
from backend.application.api.routers import artist_page_router
from backend.application.api.routers import register_router
from backend.application.api.routers import auth_router
from backend.application.api.routers import account_router
from backend.application.api.routers import upload_photo_router
from backend.application.api.routers import search_router
from backend.application.api.routers import likes_router
from backend.application.api.routers import subscribes_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого источника
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить любые заголовки
)

app.include_router(painting_router.router)
app.include_router(artist_router.router)
app.include_router(artist_page_router.router)
app.include_router(register_router.router)
app.include_router(auth_router.router)
app.include_router(account_router.router)
app.include_router(upload_photo_router.router)
app.include_router(search_router.router)
app.include_router(likes_router.router)
app.include_router(subscribes_router.router)



@app.get("/")
async def home():
    return {"message": "Добро пожаловать в API Artloom!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
