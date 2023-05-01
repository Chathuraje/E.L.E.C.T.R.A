from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum
from app.libraries import config
import pytz
import uuid

class Roles(str, Enum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: Optional[Roles] = Roles.user
    disabled: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now(tz=pytz.timezone(config.APP_TIMEZONE))
    updated_at: Optional[datetime] = datetime.now(tz=pytz.timezone(config.APP_TIMEZONE))

class UserCreate(UserBase):
    password: str
    
    
class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: Optional[Roles] = None
    disabled: Optional[bool] = None
    updated_at: Optional[datetime] = datetime.now(tz=pytz.timezone(config.APP_TIMEZONE))


# View Models
class User(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
        
        
class ShowUser(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True