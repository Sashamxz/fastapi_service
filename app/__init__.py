from fastapi import FastAPI
from database import engine, SessionLocal, Base

app = FastAPI()




### DB
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
