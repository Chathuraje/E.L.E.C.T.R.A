from fastapi import APIRouter
from .scraping.routers import router as scraping_router
from .nlp.routers import router as nlp_router
from .synthesize.routers import router as synthesize_router
from .storage.routers import router as storage_router

router = APIRouter(
    prefix="/tools",
)

router.include_router(scraping_router)
router.include_router(nlp_router)
router.include_router(synthesize_router)
router.include_router(storage_router)


