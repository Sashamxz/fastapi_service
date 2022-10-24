from fastapi import FastAPI
from app import models 
from app.database import engine, SessionLocal, Base
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import router




models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_app():
    app = FastAPI()

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.include_router(router)  
    return app






