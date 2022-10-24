from fastapi import FastAPI
from app import models 
from app.database import engine, SessionLocal, Base
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")



### DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



