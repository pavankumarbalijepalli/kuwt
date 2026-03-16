import os
# os.chdir('..')

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from brains.gemini import get_gemini_model, get_gemini_3_1_flash_lite
from models.linkedin import LinkedInPost
from models.instagram import ReelScript
from models.twitter import TwitterThread
from models.youtube import YouTubeScript
from models.social import SocialMediaResponse
from prompts.social_media import (
    LINKEDIN_PROMPT,
    INSTAGRAM_PROMPT,
    TWITTER_PROMPT,
    YOUTUBE_PROMPT,
)
from tools.fetch_topics import fetch_topics
from datetime import datetime as dt
from utils.logger import log
from utils.paths import ASSETS_OUTPUT_DIR
import json

# llm = get_gemini_model('TEACHER_GEMINI')
llm = get_gemini_3_1_flash_lite()

teacher_on_linkedin = create_agent(
    name="teacher_on_linkedin",
    model=llm,
    system_prompt=LINKEDIN_PROMPT + "\n" + "CURRENT REQUIREMENT: Linkedin Post",
    # tools=[fetch_topics],
    response_format=LinkedInPost,
)

teacher_on_instagram = create_agent(
    name="teacher_on_instagram",
    model=llm,
    system_prompt=INSTAGRAM_PROMPT + "\n" + "CURRENT REQUIREMENT: Instagram Reel",
    # tools=[fetch_topics],
    response_format=ReelScript,
)

teacher_on_twitter = create_agent(
    name="teacher_on_twitter",
    model=llm,
    system_prompt=TWITTER_PROMPT + "\n" + "CURRENT REQUIREMENT: Twitter Thread",
    # tools=[fetch_topics],
    response_format=TwitterThread,
)

teacher_on_youtube = create_agent(
    name="teacher_on_youtube",
    model=llm,
    system_prompt=YOUTUBE_PROMPT + "\n" + "CURRENT REQUIREMENT: Youtube Video",
    # tools=[fetch_topics],
    response_format=YouTubeScript,
)


class Teachers:
    def __init__(self):
        self.linkedin_teacher = teacher_on_linkedin
        self.instagram_teacher = teacher_on_instagram
        self.twitter_teacher = teacher_on_twitter
        self.youtube_teacher = teacher_on_youtube
        self.content = None
        self.topics = fetch_topics.invoke({})
        self.date = dt.now().strftime("%Y%m%d")
        log("Teachers initialized")

    def run_teacher(self, teacher, retries=3):
        log(f"Running Agent: {teacher.name}")
        response = teacher.invoke(
            {
                "messages": [
                    HumanMessage(content=self.topics)
                ]
            }
        )
        if "structured_response" in response:
            return response["structured_response"]
        else:
            if retries > 0:
                log(f"Agent {teacher.name} failed. Retrying... ({3 - retries + 1}/3)")
                return self.run_teacher(teacher, retries - 1)

    def run(self, target_platforms: list[str] = None) -> SocialMediaResponse:
        if target_platforms is None:
            target_platforms = ["linkedin", "instagram", "twitter", "youtube"]
            
        linkedin_response = None
        if "linkedin" in target_platforms:
            linkedin_response = self.run_teacher(self.linkedin_teacher)
            
        instagram_response = None
        if "instagram" in target_platforms:
            instagram_response = self.run_teacher(self.instagram_teacher)
            
        twitter_response = None
        if "twitter" in target_platforms:
            twitter_response = self.run_teacher(self.twitter_teacher)
            
        youtube_response = None
        if "youtube" in target_platforms:
            youtube_response = self.run_teacher(self.youtube_teacher)
 
        log("All Agents completed. Compiling results...")
        self.content = SocialMediaResponse(
            linkedin_post=linkedin_response or LinkedInPost(hook="", context="", insight="", key_takeaways=[], closing_thought="", call_to_action="", hashtags=[]),
            instagram_post=instagram_response or ReelScript(hook_scene=None, context_scene=None, tension_scene=None, pivot_scene=None, payoff_scene=None, cta_scene=None), # type: ignore
            twitter_post=twitter_response,
            youtube_post=youtube_response or YouTubeScript(title="", target_duration_minutes=0, segments=[]),
        ).model_dump()
        self.save_content()
        return self.content

    def save_content(self):
        out_dir = ASSETS_OUTPUT_DIR / self.date
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = out_dir / "teachers.json"
        json.dump(self.content, filename.open("w", encoding="utf-8"), indent=4)
        log(f"Content saved to {filename}")
