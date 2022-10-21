from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache
from pathlib import Path
import pathlib
import os



ROOT_DIR = pathlib.Path(os.path.abspath(__file__)).parent.parent


@lru_cache
def get_env_path() -> Path:
    env_path = Path(__file__).parent.parent / ".env"
    return env_path


class Config(BaseSettings):
    """
    Settings for the application.
    """

    cart_path_prefix: Optional[str] = ""
    # Authentication
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Database
    QLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(ROOT_DIR, 'app.db')

    # Logging
    LOG_LEVEL: str = "DEBUG"
    UPLOADED_FILES_PATH = "uploaded_files/"
    class Config:
        env_file = get_env_path()


@lru_cache()
def get_settings():
    return Config()