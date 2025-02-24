from fastapi import APIRouter
from app.api.routes import health
from app.api.routes import upload
from app.api.routes import status

router = APIRouter()

router.include_router(health.router, prefix="", tags=["Health Check"])
router.include_router(upload.router, prefix="/upload", tags=["Upload"])
router.include_router(status.router, prefix="/status", tags=["Status"])