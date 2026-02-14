# import os
# os.chdir('..')

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from brains.ollama import get_ollama_model
from models.papers import LinkedInResearchPost, MediumResearchArticle, YouTubeResearchScript, InstagramResearchScript, ResearchersResponse
from prompts.papers import linkedin_prompt, medium_prompt, youtube_prompt, instagram_prompt
from tools.fetch_papers import get_papers
from datetime import datetime as dt
from utils.logger import log
import json

llm = get_ollama_model()

researcher_on_linkedin = create_agent(
    name="researcher_on_linkedin",
    model=llm,
    system_prompt=linkedin_prompt,
    response_format=LinkedInResearchPost
)

researcher_on_instagram = create_agent(
    name="researcher_on_instagram",
    model=llm,
    system_prompt=instagram_prompt,
    response_format=InstagramResearchScript
)

researcher_on_medium = create_agent(
    name="researcher_on_medium",
    model=llm,
    system_prompt=medium_prompt,
    response_format=MediumResearchArticle
)

researcher_on_youtube = create_agent(
    name="researcher_on_youtube",
    model=llm,
    system_prompt=youtube_prompt,
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
    
    def run_researcher(self, paper, researcher, retries=3):
        log(f"Running Agent: {researcher.name}")
        response = researcher.invoke(HumanMessage(content=paper))
        if 'structured_response' in response:
            return response['structured_response']
        else:
            if retries > 0:
                log(f"Agent {researcher.name} failed. Retrying... ({3 - retries + 1}/3)")
                return self.run_researcher(paper, researcher, retries - 1)
    
    def run(self) -> ResearchersResponse:
        papers = get_papers()
        if not papers:
            self.content = "No papers found for the given date."
        self.content = {}
        for paper_name, paper_content in papers.items():
            log(f"Processing paper: {paper_name}")
            linkedin_response = self.run_researcher(paper_content, self.linkedin_researcher)
            instagram_response = self.run_researcher(paper_content, self.instagram_researcher)
            medium_response = self.run_researcher(paper_content, self.medium_researcher)
            youtube_response = self.run_researcher(paper_content, self.youtube_researcher)
    
            log("Paper processed. Storing results...")
            self.content[paper_name] = ResearchersResponse(
                linkedin_post=linkedin_response,
                instagram_post=instagram_response,
                medium_post=medium_response,
                youtube_post=youtube_response
            ).model_dump()
        log("All Agents completed. Compiling results...")
        return self.content
        
    def save_content(self, filename: str = None):
        if not filename:
            filename = f"assets/output/researchers_{self.date}.json"
        json.dump(self.content, open(filename, 'w'))
        log(f"Content saved to {filename}")
        
researchers = Researchers()
researchers.run()
researchers.save_content()