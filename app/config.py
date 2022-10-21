import os
from dotenv import load_dotenv
from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache



load_dotenv()
basedir = os.path.join(os.path.dirname(__file__))


# @lru_cache()
# def get_settings():
#     return config.Settings()


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    cart_path_prefix: Optional[str] = ""
    # Authentication
    secret_key: str = os.getenv('SECRET_KEY')
   
    access_token_expire_minutes: int = 10

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Logging
    LOG_LEVEL: str = "DEBUG"
    UPLOADED_FILES_PATH = "uploaded_files/"
   
    class Config:
        env_file = ".env"

settings = Settings()