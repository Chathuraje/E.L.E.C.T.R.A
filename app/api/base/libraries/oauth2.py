from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token
from sqlalchemy.orm import Session
from ..libraries import users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(tokenstr: str = Depends(oauth2_scheme), db: Session = Depends(users.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return token.verify_token(tokenstr, credentials_exception, db)