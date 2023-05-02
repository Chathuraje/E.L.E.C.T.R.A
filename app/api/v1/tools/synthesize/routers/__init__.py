from fastapi import APIRouter
from .elevenlabs import router as elevenlabs_router

router = APIRouter(
    prefix="/synthesize",
    tags=["Synthesize"]
)

router.include_router(elevenlabs_router)