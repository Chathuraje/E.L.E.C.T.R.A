from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CollectTimeFilter(str, Enum):
    all = "all"
    year= "year" 
    month = "month" 
    week = "week" 
    day = "day" 
    hour = "hour"
    
class CollectCaregory(str, Enum):
    best = "best"
    hot= "hot" 
    new = "new" 
    rising = "rising" 
    top = "top"
    
    
# class RedditPost(Base):
class RedditPost(BaseModel):
    id: str
    title: str
    score: int
    url: str
    posted_time: int

class RedditPostCollection(BaseModel):
    data: List[RedditPost]
    