from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

DATABASE_URL = "postgres://postgres:postgres@localhost:5432/artloombd"


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["backend.domain.models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )
