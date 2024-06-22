import logging
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
    AUTH_SALT: str = bcrypt.gensalt().decode()

    @field_validator('AUTH_SALT')
    def validate_auth_salt(cls, value):
        if not value:
            logging.warning('AUTH_SALT is Empty. Generating new one...')
            return bcrypt.gensalt().decode()
        try:
            bcrypt.checkpw(b'', value.encode())
        except ValueError:
            logging.warning('Invalid AUTH_SALT. Generating new one...')
            return bcrypt.gensalt().decode()
