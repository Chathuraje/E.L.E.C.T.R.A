from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..schemas import UserCreate, ShowUser, User, UpdateUser
from sqlalchemy.orm import Session
from app.libraries import database
from ..libraries import users
from typing import List
from ..libraries import oauth2
from ..libraries import auth
from ..schemas import Roles

get_db = database.get_db
verify_role = auth.verify_role(accepted_roles=[Roles.superadmin])

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_role)]
)

# view all
@router.get("/", response_model=List[ShowUser]) 
async def get_all_user(db: Session = Depends(get_db)):
        
    return users.get_all_user(db)


# create
@router.post("/register", response_model=ShowUser)
async def create_user(request: UserCreate, db: Session = Depends(get_db)):
    
    return users.create_user(request, db)


# view one
@router.get("/{email}", response_model=ShowUser) 
async def get_user(email, db: Session = Depends(get_db)):
        
    return users.get_user(email, db)


# update one
@router.put("/{email}", response_model=ShowUser)
def update_user(email, request: UpdateUser , db: Session = Depends(get_db)):

    return users.update_user(email, request, db)


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: str, db: Session = Depends(get_db)):
   
   return users.delete_user(email, db)







