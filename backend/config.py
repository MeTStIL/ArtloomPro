import os

SITE_BASE_URL = flask_env = os.getenv('SITE_BASE_URL', 'http://127.0.0.1:5000')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLIP_MODEL_NAME = "multilingual-multimodal-clip-embed"
CLIP_MODEL_URL = f"https://clarifai.com/clarifai/main/models/{CLIP_MODEL_NAME}"
CLARIFAI_TOKENS_FILE = os.path.join(BASE_DIR, 'clarifai_tokens.txt')

HF_API_BLIP_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"

YC_STORAGE_ENDPOINT = 'https://storage.yandexcloud.net'
YC_BUCKET_NAME = 'artloom-storage'

DATABASE_URL = "postgresql://artloom:artloom@212.193.24.77:5432/artloom"
