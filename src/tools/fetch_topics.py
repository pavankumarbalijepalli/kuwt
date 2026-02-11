from langchain_core.tools import tool
from utils.logger import log
from datetime import datetime as dt
import json

@tool
def fetch_topics():
    """
      Fetch topics for today.
    """
    log("Tool Call Init: fetch_topics")
    content_map = json.load(open("assets/input/fundamentals.json", "r"))
    today = dt.now().strftime("%Y-%m-%d")
    todays_topics = content_map[today]
    log("Tool Call Finish: fetch_topics")
    return todays_topics