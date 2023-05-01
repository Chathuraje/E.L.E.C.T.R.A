import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
TEXT_TO_SPEECH_API_KEY = os.getenv('TEXT_TO_SPEECH_API_KEY')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
