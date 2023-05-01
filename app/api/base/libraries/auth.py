from .hashing import Hash
from sqlalchemy.orm import Session
from app.libraries import database
from fastapi import  Depends, status, HTTPException
from . import token
from app.models.Users import DB_User
from ..libraries import oauth2
from ..schemas import User, Roles
from typing import List

get_db = database.get_db

def login(request, db: Session = Depends(get_db)):
    login_user = db.query(DB_User).filter(DB_User.email == request.username).first()
    if not login_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Incorrect email or password")
    if not Hash.verify(login_user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Incorrect email or password")
    
    access_token = token.create_access_token(
        data={"sub": login_user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


def verify_role(accepted_roles: List[str]):
    def _verify_role(current_user: User = Depends(oauth2.get_current_user)):
        accepted_roles.append(Roles.superadmin)
        
        if current_user.roles == Roles.admin:
            accepted_roles.append(Roles.user)
        
        if current_user.roles not in accepted_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission")
        else:
            return current_user
    return _verify_role
