from fastapi import APIRouter
from .base.routers import router as base_router
from .v1 import router as v1_router

router = APIRouter()


router.include_router(v1_router)
router.include_router(base_router)