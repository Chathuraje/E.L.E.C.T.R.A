from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# class ScreenShot(Base):
class ScreenShot(BaseModel):
    url: str
    
class ScreenShotReddit(ScreenShot):
    commentsid: List[str]