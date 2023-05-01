from fastapi import APIRouter
from .chatgpt import router as chatgpt_router

router = APIRouter()

router.include_router(chatgpt_router)