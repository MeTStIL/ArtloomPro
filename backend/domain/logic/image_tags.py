import requests
from time import sleep

from backend.api_keys import HUGGING_FACE_TOKEN, MISTRAL_API_KEY
from backend.config import HF_API_BLIP_URL, MISTRAL_API_URL, MISTRAL_MODEL


def get_image_tags(image_url: str):
    image_description = _get_image_description(image_url)
    return _get_tags_by_description(image_description)


def _get_image_description(image_url: str):
    headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
    payload = {
        "inputs": {"image": image_url}
    }

    max_attempts = 6
    for attempt in range(max_attempts):
        try:
            response = requests.post(HF_API_BLIP_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()[0]['generated_text']
            sleep(0.1)
        except Exception as e:
            sleep(0.1)
    return None


def _get_tags_by_description(description: str):
    prompt = (
        f'Это описание картины: "{description}". Напиши в строку список из топ 5 тегов '
        f'на русском, которые лучше всего будут описывать эту картину. '
        f'Теги должны в основном описывать объекты, цвета и действия, '
        f'которые изображены на картине. Избегай общих или абстрактных тегов, таких как '
        f'"пейзаж", "картина", "искусство", "фон", "линия" и тп. Теги должны быть '
        f'неповторяющимися по смыслу, каждый тег - одно слово с маленькой буквы, '
        f'склеивать несколько слов в один тег нельзя. '
        f'В твоем ответе должны быть только теги через ; без пробелов, ничего лишнего.'
    )

    retries_count = 0
    tags = None
    while tags is None or len(tags) != 5:
        tags = _send_message_to_mistral(prompt).split(';')
        if retries_count >= 5:
            break
    return tags


def _send_message_to_mistral(prompt, temperature=0.7, max_tokens=200):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MISTRAL_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    max_attempts = 6
    for attempt in range(max_attempts):
        try:
            response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
            if response.status_code == 200:
                return response.json().get_artist_by_id("choices")[0].get_artist_by_id("message").get_artist_by_id("content")
            sleep(0.1)
        except Exception as e:
            sleep(0.1)

    return None

