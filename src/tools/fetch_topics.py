from langchain_core.tools import tool
from utils.logger import log
from datetime import datetime as dt
import json
import redis
import os

from dotenv import load_dotenv
load_dotenv('../../.env')

r = redis.Redis.from_url(os.environ["REDIS_URL"])

@tool
def fetch_topics():
    """
      Fetch topics for today.
    """
    log("Tool Call Init: fetch_topics")
    content_map = json.loads(r.get('fundamentals'))
    today = dt.now().strftime("%Y-%m-%d")
    todays_topics = content_map[today]
    log("Tool Call Finish: fetch_topics")
    return todays_topics