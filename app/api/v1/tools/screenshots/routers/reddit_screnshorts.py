from fastapi import APIRouter, Depends
from ..libraries import reddit_screnshorts
from ..schemas import ScreenShot, ScreenShotReddit
from app.libraries import database
from .....base.schemas import User
from app.api.base.schemas import Roles
from app.api.base.libraries import auth
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/reddit"
)

get_db = database.get_db
verify_role = auth.verify_role(accepted_roles=[Roles.user])


@router.post("/")
async def capture_reddit_text_based_post(
    screenShot: ScreenShotReddit, 
    current_user: User = Depends(verify_role), 
    db: Session = Depends(get_db)
):
    
    return await reddit_screnshorts.capture_reddit_text_based_post(screenShot, current_user, db)
