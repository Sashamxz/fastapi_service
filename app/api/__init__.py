from fastapi import APIRouter
from app.api.routes import router as file_router


router = APIRouter(prefix="/api", tags=["API"])
router.include_router(file_router)