from fastapi import APIRouter
from .reddit import router as reddit_router

router = APIRouter()

router.include_router(reddit_router)