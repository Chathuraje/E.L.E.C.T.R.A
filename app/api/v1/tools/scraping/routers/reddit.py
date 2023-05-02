# Tool: Scraping/Reddit
main_tool_name = "scraping"
sub_tool_name = "reddit"
description = "Scrape text-based reddit posts and comments"

# Output file format
mime_type = "NA"
output_file_format = "NA"
system_folder_name = "NA"

# Usefull Information
use_db = False
use_storage = False

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