# ::TODO:: Need to handel the exception and return the error message to the user
# ::TODO:: Need to add the way to do profanity check another way to do it


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


from fastapi import HTTPException, status
from app.libraries import secrets, config
import praw, prawcore
import pandas as pd
from praw.models import MoreComments
from bs4 import BeautifulSoup
from markdown import markdown
import re
from ..schemas import RedditPost, RedditPostCollection, RedditComments, RedditCommentsCollection

def __getRedditClient():
    try: 
        reddit_clint = praw.Reddit(
            client_id=secrets.REDDIT_CLIENT_ID,
            client_secret=secrets.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT
        )
        return reddit_clint
    except prawcore.exceptions.Forbidden as e:
        pass
    

def get_reddit_text_titles(subreddit: str, limit: int, time_filter: str, category: str, nsfw: bool):
    limit = limit*3
    profinity_data = pd.read_csv("app/static/datasets/profinity_check.csv")
    profinity_words = set(profinity_data["word"].str.lower())
    
    try:
        reddit = __getRedditClient()
        subreddit = reddit.subreddit(subreddit)
    except Exception as e:
        pass
    
    if category == "best":
        posts = subreddit.best(limit=limit)
    elif category == "hot":
        posts = subreddit.hot(limit=limit)
    elif category == "new":
        posts = subreddit.new(limit=limit)
    elif category == "rising":
        posts = subreddit.rising(limit=limit)
    elif category == "top":
        if time_filter == "all" or time_filter == "year" or time_filter == "month" or time_filter == "week" or time_filter == "day" or time_filter == "hour":
            posts = subreddit.top(time_filter=time_filter, limit=limit)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Time filter not found: Only all, year, month, week, day, hour are allowed")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found: Only best, hot, new, rising, top are allowed")
    
    data = []
    for post in posts:
        if post.over_18 and not nsfw:
            continue
        
        if post.stickied:
            continue
         
        if any(word in post.title.lower() for word in profinity_words):
            continue
            
        data.append(RedditPost(
            id=post.id,
            title=post.title,
            score=post.score,
            url=post.url,
            posted_time=post.created_utc
        ))
        
        if len(data) == int(limit//3):
            break
        
    data = sorted(data, key=lambda x: x.score, reverse=True)
    return RedditPostCollection(data=data)


def __markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)
    html = re.sub(r'~~(.*?)~~', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text


def get_text_comments_data(post_id: str, limit: int, min_words: int, max_words: int):
    reddit = __getRedditClient()
    
    try:
        submission = reddit.submission(id=post_id)
    except Exception as e:
        pass
    
    submission.comments.replace_more(limit=10)
    
    profinity_data = pd.read_csv("app/static/datasets/profinity_check.csv")
    profinity_words = set(profinity_data["word"].str.lower())
    
    data = []
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        if comment.banned_by is not None:
            continue
        if comment.body == "[removed]":
            continue
        if comment.body == "[deleted]":
            continue
        if any(word in comment.body.lower() for word in profinity_words):
            continue
        wordCount = len(comment.body)
        if (wordCount > max_words) or (wordCount < min_words):
            continue
            
            
        comments_body = __markdown_to_text(comment.body)
        
        data.append(RedditComments(
            id=comment.id,
            body=comments_body,
            score=comment.score,
            posted_time=comment.created_utc
        ))
        
        if len(data) == limit:
            break
    data = sorted(data, key=lambda x: x.score, reverse=True)
    return RedditCommentsCollection(data=data)