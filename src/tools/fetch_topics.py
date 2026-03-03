from langchain_core.tools import tool
from utils.logger import log
from datetime import datetime as dt
import json
import redis
import os

def _get_redis() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL environment variable is required.")
    return redis.Redis.from_url(redis_url)


def _loads_maybe_bytes(value):
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8")
    return json.loads(value)


@tool
def fetch_topics():
    """
    Fetch topics for today.
    """
    log("Tool Call Init: fetch_topics")
    r = _get_redis()
    content_map = _loads_maybe_bytes(r.get("fundamentals"))
    if not content_map:
        raise RuntimeError("Redis key 'fundamentals' is missing or empty.")
    today = dt.now().strftime("%Y-%m-%d")
    if today not in content_map:
        raise RuntimeError(f"Redis key 'fundamentals' has no entry for {today}.")
    todays_topics = content_map[today]
    log("Tool Call Finish: fetch_topics")
    return todays_topics
