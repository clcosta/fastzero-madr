import logging
import random
import string
from pathlib import Path

import bcrypt
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logging = logging.getLogger(__name__)


class Configs(BaseSettings):

    BASE_URL: Path = Path(__file__).parent.parent.parent

    model_config = SettingsConfigDict(
        env_file=BASE_URL / '.env', env_file_encoding='utf-8', extra='ignore'
    )

    ## DATABASE
    DATABASE_URL: str = 'sqlite:///db.sqlite3'

    ## AUTH
    AUTH_SECRET_KEY: str = ''
    AUTH_ALGORITHM: str = 'HS256'
    AUTH_JWT_EXPIRES_MINUTES: int = 60
    AUTH_SALT: str = bcrypt.gensalt().decode()

    @field_validator('AUTH_SALT')
    def validate_auth_salt(cls, value):  # pragma: no coverage
        if not value:
            logging.warning('AUTH_SALT is Empty. Generating new one...')
            return bcrypt.gensalt().decode()
        try:
            bcrypt.checkpw(b'', value.encode())
            return value
        except ValueError:
            logging.warning('Invalid AUTH_SALT. Generating new one...')
            return bcrypt.gensalt().decode()

    @staticmethod
    def _gen_secret_key(size: int = 24) -> str:  # pragma: no coverage
        return ''.join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation,
                k=size,
            )
        )

    @field_validator('AUTH_SECRET_KEY')
    def validate_auth_secret_key(cls, value):  # pragma: no coverage
        if not value:
            logging.warning('AUTH_SECRET_KEY is Empty. Generating new one...')
            return cls._gen_secret_key()
        return value
