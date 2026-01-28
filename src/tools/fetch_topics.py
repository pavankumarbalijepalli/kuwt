from langchain_core.tools import tool
import json

@tool
def fetch_topics():
    """
      Fetch topics for today.
    """
    content_map = json.load(open("assets/fundamentals.json", "r"))
    todays_topics = content_map['not_started'][0]
    content_map['not_started'] = content_map['not_started'][1:]
    content_map['completed'].append(todays_topics)
    with open("assets/fundamentals.json", "w") as f:
        json.dump(content_map, f, indent=4)
    return todays_topics