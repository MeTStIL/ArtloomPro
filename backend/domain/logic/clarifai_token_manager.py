import os
import logging
from typing import List, Optional
from clarifai.client.model import Model
from backend.config import CLIP_MODEL_URL, CLARIFAI_TOKENS_FILE

logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self, tokens_file: str = CLARIFAI_TOKENS_FILE):
        self.tokens_file = tokens_file
        self.used_tokens: List[str] = []
        self.active_tokens: List[str] = []
        self.current_token: Optional[str] = None
        self._load_tokens()
        self._initialize_model()

    def _load_tokens(self):
        if not os.path.exists(self.tokens_file):
            raise FileNotFoundError(f"Token file {self.tokens_file} not found")

        with open(self.tokens_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("- "):
                    token = line[2:].strip()
                    if token:
                        self.used_tokens.append(token)
                else:
                    self.active_tokens.append(line)

        if not self.active_tokens:
            raise ValueError("No active tokens available in the tokens file")

    def _save_tokens(self):
        with open(self.tokens_file, 'w') as f:
            for token in self.used_tokens:
                f.write(f"- {token}\n")
            for token in self.active_tokens:
                f.write(f"{token}\n")

    def _initialize_model(self):
        if self.active_tokens:
            self.current_token = self.active_tokens[0]
            try:
                self.model = Model(
                    url=CLIP_MODEL_URL,
                    pat=self.current_token
                )
            except Exception as e:
                logger.error(f"clarifai token manager: Error initializing model with token: {str(e)}")
                self._handle_token_error()

    def _switch_token(self):
        if self.current_token:
            self.used_tokens.append(self.current_token)
            self.active_tokens.pop(0)

        self._save_tokens()

        if self.active_tokens:
            self.current_token = self.active_tokens[0]
            self.model = Model(
                url=CLIP_MODEL_URL,
                pat=self.current_token
            )
        else:
            raise Exception("All clarifai tokens exhausted")

    def _handle_token_error(self):
        self._switch_token()
        logger.warning(f"clarifai token manager: Switched to new token: {self.current_token}. {len(self.active_tokens)} remaining")

    def get_model(self):
        return self.model

    def clarifai_api_error_handler(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "Account limits exceeded" in str(e) or "plan" in str(e).lower():
                    self._handle_token_error()
                    return wrapper(*args, **kwargs)
                raise
        return wrapper

token_manager = TokenManager()