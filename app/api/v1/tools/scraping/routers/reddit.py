from fastapi import APIRouter, Depends
from ..libraries import reddit
from ..schemas import CollectTimeFilter, CollectCaregory
from app.api.base.libraries import auth
from app.api.base.schemas import Roles
from .....base.schemas import User

verify_role = auth.verify_role(accepted_roles=[Roles.user])
router = APIRouter(
    prefix="/reddit",
    tags=["Reddits"]
)


@router.get("/collect")
def get_reddit_text_titles(
    subreddit: str="AskReddit", 
    limit: int=10, 
    time_filter: CollectTimeFilter="day", 
    category: CollectCaregory="top", 
    nsfw: bool=False,
    current_user: User = Depends(verify_role)
):
    
    return reddit.get_reddit_text_titles(subreddit, limit, time_filter, category, nsfw)

@router.get("/collect/{post}")
def get_text_comments_data(
    post: str, 
    limit: int=10, 
    min_words: int=1, 
    max_words: int=25,
    current_user: User = Depends(verify_role)
):
    
    return reddit.get_text_comments_data(post, limit, min_words, max_words)