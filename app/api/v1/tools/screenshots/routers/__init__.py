from fastapi import APIRouter
from .screnshorts import router as screenshots_router
from .reddit_screnshorts import router as reddit_screnshorts_router

router = APIRouter(
    prefix="/screenshots",
    tags=["Screenshot"]
)

router.include_router(screenshots_router)
router.include_router(reddit_screnshorts_router)