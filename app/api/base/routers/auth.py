from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.libraries import database
from sqlalchemy.orm import Session
from ..libraries import auth
from ..schemas import ShowUser, User
from ..libraries import oauth2

get_db = database.get_db

router = APIRouter(
    tags=["Authentications"]
)


@router.post("/login")
async def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    return auth.login(request, db)

@router.post("/myaccount", response_model=ShowUser)
async def show_my_account(current_user: User = Depends(oauth2.get_current_user)):
    
    return current_user