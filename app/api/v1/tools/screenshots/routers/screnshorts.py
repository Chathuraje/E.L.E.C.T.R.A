from fastapi import APIRouter, Depends
from ..libraries import screnshorts
from ..schemas import ScreenShot, ScreenShotReddit
from app.libraries import database
from .....base.schemas import User
from app.api.base.schemas import Roles
from app.api.base.libraries import auth
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db
verify_role = auth.verify_role(accepted_roles=[Roles.user])

@router.get("/")
async def capture_site_view(
    url: str,
    current_user: User = Depends(verify_role),
    db: Session = Depends(get_db)
):
    
    return await screnshorts.capture_site_view(url, current_user, db)