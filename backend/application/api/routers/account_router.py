from fastapi import APIRouter
from backend.domain.models.account import Account

router = APIRouter()


@router.get("/accounts/{account_id}", response_model=Account)
async def get_artist(account_id: int):
    account_data = {
        "id": account_id,
        "login": "YuriRomashov",
        "avatar_img_url": "https://cdn.buildin.ai/s3/582e7eb9-1943-4879-a6f8-ac4ae73a"
                   "10dd/photo_2024-11-21_13-29-19.jpg?time=1740576600&token=d"
                   "83ede8d3bde09f07350398a105f8987&role=free&x-oss-process=im"
                   "age/quality,q_100/",
        "favourite_painting_ids": [1, 2, 3],
        "subscribed_artist_ids": [777, 2, 1],
    }
    return Account(**account_data)
