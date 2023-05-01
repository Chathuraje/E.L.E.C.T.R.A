from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# class Audio(Base):
class Audio(BaseModel):
    text: str