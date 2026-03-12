from time import sleep
import os
# os.chdir('..')

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from brains.gemini import get_gemini_model, get_gemini_3_1_flash_lite
from models.linkedin import LinkedInPost
from models.instagram import ReelScript
from models.medium import MediumArticle
from models.youtube import YouTubeScript
from models.social import SocialMediaResponse
from prompts.social_media import (
    LINKEDIN_PROMPT,
    INSTAGRAM_PROMPT,
    MEDIUM_PROMPT,
    YOUTUBE_PROMPT,
)
from tools.fetch_papers import get_papers
from datetime import datetime as dt
from utils.logger import log
from utils.paths import ASSETS_OUTPUT_DIR
import json

# llm = get_gemini_model('RESEARCHER_GEMINI')
llm = get_gemini_3_1_flash_lite()

researcher_on_linkedin = create_agent(
    name="researcher_on_linkedin",
    model=llm,
    system_prompt=LINKEDIN_PROMPT + "\n" + "CURRENT REQUIREMENT: Linkedin Post",
    response_format=LinkedInPost,
)

researcher_on_instagram = create_agent(
    name="researcher_on_instagram",
    model=llm,
    system_prompt=INSTAGRAM_PROMPT + "\n" + "CURRENT REQUIREMENT: Instagram Reel",
    response_format=ReelScript,
)

researcher_on_medium = create_agent(
    name="researcher_on_medium",
    model=llm,
    system_prompt=MEDIUM_PROMPT + "\n" + "CURRENT REQUIREMENT: Medium Article",
    response_format=MediumArticle,
)

researcher_on_youtube = create_agent(
    name="researcher_on_youtube",
    model=llm,
    system_prompt=YOUTUBE_PROMPT + "\n" + "CURRENT REQUIREMENT: Youtube Video",
    response_format=YouTubeScript,
)


class Researchers:
    def __init__(self):
        self.linkedin_researcher = researcher_on_linkedin
        self.instagram_researcher = researcher_on_instagram
        self.medium_researcher = researcher_on_medium
        self.youtube_researcher = researcher_on_youtube
        self.content = None
        self.date = dt.now().strftime("%Y%m%d")
        self.papers = get_papers()
        log("Researchers initialized")

    def run_researcher(self, paper, researcher, retries=3):
        log(f"Running Agent: {researcher.name}")
        response = researcher.invoke({"messages": [HumanMessage(content=paper)]})
        if "structured_response" in response:
            return response["structured_response"]
        else:
            if retries > 0:
                log(
                    f"Agent {researcher.name} failed. Retrying... ({3 - retries + 1}/3)"
                )
                return self.run_researcher(paper, researcher, retries - 1)

    def run(self) -> dict[str, SocialMediaResponse]:
        if not self.papers:
            # self.content = "No papers found for the given date."
            log("No papers found for the given date.")
            return self.content
        self.content = {}
        for paper_name, paper_content in self.papers.items():
            log(f"Processing paper: {paper_name}")
            linkedin_response = self.run_researcher(
                paper_content, self.linkedin_researcher
            )
            instagram_response = self.run_researcher(
                paper_content, self.instagram_researcher
            )
            medium_response = self.run_researcher(paper_content, self.medium_researcher)
            youtube_response = self.run_researcher(
                paper_content, self.youtube_researcher
            )

            log("Paper processed. Storing results...")
            self.content[paper_name] = SocialMediaResponse(
                linkedin_post=linkedin_response,
                instagram_post=instagram_response,
                medium_post=medium_response,
                youtube_post=youtube_response,
            ).model_dump()
            sleep(60)  # Sleep for 60 seconds to avoid rate limits
        log("All Agents completed. Compiling results...")
        self.save_content()
        return self.content

    def save_content(self):
        out_dir = ASSETS_OUTPUT_DIR / self.date
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = out_dir / "researchers.json"
        json.dump(self.content, filename.open("w", encoding="utf-8"), indent=4)
        log(f"Content saved to {filename}")
