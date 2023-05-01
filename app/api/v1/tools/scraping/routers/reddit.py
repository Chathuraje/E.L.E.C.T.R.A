from fastapi import APIRouter
from ..libraries import reddit
from ..schemas import CollectTimeFilter, CollectCaregory

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
    nsfw: bool=False
):
    
    return reddit.get_reddit_text_titles(subreddit, limit, time_filter, category, nsfw)

@router.get("/collect/{post}")
def get_text_comments_data(post: str, limit: int=10, min_words: int=1, max_words: int=25):
    
    return reddit.get_text_comments_data(post, limit, min_words, max_words)