from fastapi import APIRouter
from .tools import router as tools_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(tools_router)