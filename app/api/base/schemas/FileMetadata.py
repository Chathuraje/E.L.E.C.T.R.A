from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum
from app.libraries import config
import pytz
import uuid


class BaseFileMetadata(BaseModel):
    id: str
    real_name: str
    file_size: int
    file_type: str
    file_description: Optional[str]
    tool_name: str
    file_path: str
    created_at: Optional[datetime] = datetime.now(tz=pytz.timezone(config.APP_TIMEZONE))

class FileMetadata(BaseFileMetadata):
    owner_id: uuid.UUID