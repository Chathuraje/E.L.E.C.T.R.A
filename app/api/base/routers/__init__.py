from fastapi import APIRouter
from .root import router as root_roouters
from .auth import router as auth_routers
from .users import router as user_routers

router = APIRouter()

router.include_router(root_roouters)
router.include_router(auth_routers)
router.include_router(user_routers)