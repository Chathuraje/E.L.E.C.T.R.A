from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .hashing import Hash
from app.libraries import database
from app.models.Users import DB_User
from ..schemas import UserCreate, ShowUser, UpdateUser, Roles
from datetime import datetime
import os
import uuid
from app.libraries import config
LOCAL_STORAGE_LOCATION = config.LOCAL_STORAGE_LOCATION


get_db = database.get_db


def __get_user(email, db: Session = Depends(get_db)):
    user = db.query(DB_User).filter(DB_User.email == email).first()
    
    return user


def __create_user_folder(user_id):
    user_dir = os.path.join(LOCAL_STORAGE_LOCATION, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        
    sys_dir = os.path.join(user_dir, ".sys")
    if not os.path.exists(sys_dir):
        os.makedirs(sys_dir)
        

def create_user(request:UserCreate, db: Session = Depends(get_db)):
    user = __get_user(request.email, db)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = DB_User(
        email=request.email, 
        first_name=request.first_name, 
        last_name=request.last_name, 
        password=Hash.bcrypt(request.password),
        roles=request.roles, 
        disabled=request.disabled, 
        created_at=request.created_at,
        id=str(uuid.uuid4())
    )
   
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        __create_user_folder(new_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating user, check the database connection")
    
    return new_user


def get_user(email, db: Session = Depends(get_db)):
    user = __get_user(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with email {email} not found")
        
    return user


def get_all_user(db: Session = Depends(get_db)):
    users = db.query(DB_User).all()
        
    return users


def update_user(email: str, request: UpdateUser, db: Session = Depends(get_db)):
    # Check if any update values are available
    if not (request.first_name or request.last_name or request.roles or request.disabled or request.password or request.email):
        raise HTTPException(status_code=400, detail="No update values provided")
    
    user = __get_user(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )

    if request.email:
        existing_user = __get_user(request.email, db)
        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )
        user.email = request.email

    if request.first_name:
        user.first_name = request.first_name

    if request.last_name:
        user.last_name = request.last_name

    if request.password:
        user.password = Hash.bcrypt(request.password)

    if request.roles is not None:
        user.roles = request.roles

    if request.disabled is not None:
        user.disabled = request.disabled

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return user



def delete_user(email, db):
    user = __get_user(email, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )
    
    if user.roles == Roles.superadmin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {email} is a superadmin and cannot be deleted",
        )
        
    db.delete(user)
    db.commit()
    
    return "User deleted successfully"



async def get_user_storage_path(current_user, system=False):
    if system:
        return os.path.join(LOCAL_STORAGE_LOCATION, str(current_user.id), ".sys")
    
    return os.path.join(LOCAL_STORAGE_LOCATION, str(current_user.id))