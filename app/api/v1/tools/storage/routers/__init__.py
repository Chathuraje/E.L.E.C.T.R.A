from fastapi import APIRouter
from .storage import router as storage_router

router = APIRouter()

router.include_router(storage_router)