import os
from re import S
from dotenv import load_dotenv
from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache

import sqlalchemy



load_dotenv()
basedir = os.path.join(os.path.dirname(__file__))


# @lru_cache()
# def get_settings():
#     return config.Settings()


class Settings(BaseSettings):
    """
    Settings for the application.
    """
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    cart_path_prefix: Optional[str] = ""
    # Authentication
    secret_key: str = os.getenv('SECRET_KEY')
   
    access_token_expire_minutes: int = 10

    # Database
    sqlalchemy_database_url: str = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Logging
    LOG_LEVEL: str = "DEBUG"
    UPLOADED_FILES_PATH: str = "uploaded_files/"
   
    class Config:
        env_file = ".env"

settings = Settings()