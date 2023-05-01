from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# class MetaData(Base): using ChatGPT
class MetaData(BaseModel):
    platform: str
    prompt_type: str
    video_name: str
    min_length: int
    max_length: int
    limit: int
    additional: str = None