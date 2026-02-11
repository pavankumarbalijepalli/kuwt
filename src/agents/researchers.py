import os
os.chdir('..')

from langchain.agents import create_agent
from brains.ollama import get_ollama_model
from models.papers import LinkedInResearchPost, MediumResearchArticle, YouTubeResearchScript, InstagramResearchScript, ResearchersResponse
from prompts.papers import linkedin_prompt, medium_prompt, youtube_prompt, instagram_prompt
from tools.fetch_papers import download_hf_papers
from datetime import datetime as dt
from utils.logger import log
import json

llm = get_ollama_model()

researcher_on_linkedin = create_agent(
    name="researcher_on_linkedin",
    model=llm,
    system_prompt=linkedin_prompt,
    tools=[fetch_topics],
    response_format=LinkedInResearchPost
)

researcher_on_instagram = create_agent(
    name="researcher_on_instagram",
    model=llm,
    system_prompt=instagram_prompt,
    tools=[fetch_topics],
    response_format=InstagramResearchScript
)

researcher_on_medium = create_agent(
    name="researcher_on_medium",
    model=llm,
    system_prompt=medium_prompt,
    tools=[fetch_topics],
    response_format=MediumResearchArticle
)

researcher_on_youtube = create_agent(
    name="researcher_on_youtube",
    model=llm,
    system_prompt=youtube_prompt,
    tools=[fetch_topics],
    response_format=YouTubeResearchScript
)

class Researchers:
    def __init__(self):
        self.linkedin_researcher = researcher_on_linkedin
        self.instagram_researcher = researcher_on_instagram
        self.medium_researcher = researcher_on_medium
        self.youtube_researcher = researcher_on_youtube
        self.content = None
        self.date = dt.now().strftime("%Y%m%d")
        log("Researchers initialized")
    
    def run_researcher(self, researcher, retries=3):
        log(f"Running Agent: {researcher.name}")
        response = researcher.invoke({})
        if 'structured_response' in response:
            return response['structured_response']
        else:
            if retries > 0:
                log(f"Agent {researcher.name} failed. Retrying... ({3 - retries + 1}/3)")
                return self.run_researcher(researcher, retries - 1)
    
    def run(self) -> ResearchersResponse:
        linkedin_response = self.run_researcher(self.linkedin_researcher)
        instagram_response = self.run_researcher(self.instagram_researcher)
        medium_response = self.run_researcher(self.medium_researcher)
        youtube_response = self.run_researcher(self.youtube_researcher)
    
        log("All Agents completed. Compiling results...")
        self.content = ResearchersResponse(
            linkedin_post=linkedin_response,
            instagram_post=instagram_response,
            medium_post=medium_response,
            youtube_post=youtube_response
        )
        return self.content
        
    def save_content(self, filename: str = None):
        if not filename:
            filename = f"output/researchers_{self.date}.json"
        json.dump(self.content.model_dump(), open(filename, 'w'))
            
# researchers = Researchers()
# researchers.run()
# researchers.save_content("agents/output/researchers_response.json")