import databases
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database = databases.Database(Config.SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_some_thread": False},  # Add it if you use SQLite
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()