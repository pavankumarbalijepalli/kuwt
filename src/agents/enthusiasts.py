import os
# os.chdir('..')

import json
from datetime import datetime as dt
from time import sleep
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from brains.mistral import get_mistral_model
from models.tools_and_news import (
    InstagramNewsVideo,
    LinkedinNewsPost,
    MediumNewsPost,
    YoutubeNewsVideo,
)
from prompts.tools_and_news import TOOLS_AND_NEWS_PROMPT
from tools.fetch_tools_and_news import fetch_news_repos
from utils.logger import log
from utils.paths import ASSETS_OUTPUT_DIR

llm = get_mistral_model()

enthusiast_on_linkedin = create_agent(
    name="enthusiast_on_linkedin",
    model=llm,
    system_prompt=TOOLS_AND_NEWS_PROMPT + "\n" + "CURRENT REQUIREMENT: Linkedin Post",
    response_format=LinkedinNewsPost,
)

enthusiast_on_instagram = create_agent(
    name="enthusiast_on_instagram",
    model=llm,
    system_prompt=TOOLS_AND_NEWS_PROMPT + "\n" + "CURRENT REQUIREMENT: Instagram Reel",
    response_format=InstagramNewsVideo,
)

enthusiast_on_medium = create_agent(
    name="enthusiast_on_medium",
    model=llm,
    system_prompt=TOOLS_AND_NEWS_PROMPT + "\n" + "CURRENT REQUIREMENT: Medium Article",
    response_format=MediumNewsPost,
)

enthusiast_on_youtube = create_agent(
    name="enthusiast_on_youtube",
    model=llm,
    system_prompt=TOOLS_AND_NEWS_PROMPT + "\n" + "CURRENT REQUIREMENT: Youtube Video",
    response_format=YoutubeNewsVideo,
)


class Enthusiasts:
    def __init__(self):
        self.linkedin_enthusiast = enthusiast_on_linkedin
        self.instagram_enthusiast = enthusiast_on_instagram
        self.medium_enthusiast = enthusiast_on_medium
        self.youtube_enthusiast = enthusiast_on_youtube
        self.content = None
        self.date = dt.now().strftime("%Y%m%d")
        self.news, self.repos = fetch_news_repos()
        log("Enthusiasts initialized")

    def run_enthusiast(self, topic, enthusiast, retries=3):
        log(f"Running Agent: {enthusiast.name}")
        response = enthusiast.invoke({"messages": [HumanMessage(content=str(topic))]})
        if "structured_response" in response:
            return response["structured_response"]
        else:
            if retries > 0:
                log(
                    f"Agent {enthusiast.name} failed. Retrying... ({3 - retries + 1}/3)"
                )
                return self.run_enthusiast(topic, enthusiast, retries - 1)

    def run(self):
        raw_content = {
            "news": {"news": {"content": self.news.get("content", [])}},
            "repos": self.repos,
        }
        if not raw_content["news"]['news']['content'] and not raw_content["repos"]:
            self.content = "No news or repos found for the given date."
            return self.content
        self.content = {"news": {}, "repos": {}}

        for topic_name, topic_dictionary in raw_content.items():
            log(f"Processing {topic_name}: {len(topic_dictionary)} items")
            for item_name, item_content in topic_dictionary.items():
                log(f"Processing Item: {item_name}")
                linkedin_response = self.run_enthusiast(
                    item_content, self.linkedin_enthusiast
                )
                sleep(60)  # Sleep for 60 seconds to avoid rate limits
                instagram_response = self.run_enthusiast(
                    item_content, self.instagram_enthusiast
                )
                sleep(60)  # Sleep for 60 seconds to avoid rate limits
                youtube_response = self.run_enthusiast(
                    item_content, self.youtube_enthusiast
                )
                sleep(60)  # Sleep for 60 seconds to avoid rate limits
                self.content[topic_name][item_name] = {
                    "linkedin_post": linkedin_response.model_dump(),
                    "instagram_post": instagram_response.model_dump(),
                    "youtube_video": youtube_response.model_dump(),
                }
        log("All Agents completed. Compiling results...")
        self.save_content()
        return self.content

    def save_content(self):
        out_dir = ASSETS_OUTPUT_DIR / self.date
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = out_dir / "enthusiasts.json"
        json.dump(self.content, filename.open("w", encoding="utf-8"), indent=4)
        log(f"Content saved to {filename}")
