from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# class RedditPost(Base):
class RedditComments(BaseModel):
    id: str
    body: str
    score: int
    posted_time: int

class RedditCommentsCollection(BaseModel):
    data: List[RedditComments]