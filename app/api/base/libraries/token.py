from datetime import datetime, timedelta
from app.libraries import config, secrets
from jose import JWTError, jwt
from ..schemas import TokenData
from ..libraries import users
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secrets.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db: Session = Depends(users.get_db)):
    try:
        payload = jwt.decode(token, secrets.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = users.get_user(email=token_data.email, db=db)
    if user is None:
        raise credentials_exception
    return user