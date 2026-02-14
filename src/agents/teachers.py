# import os
# os.chdir('..')

from langchain.agents import create_agent
from brains.ollama import get_ollama_model
from models.fundamentals import LinkedinResponse, MediumResponse, YoutubeResponse, InstagramResponse, TeachersResponse
from prompts.fundamentals import linkedin_prompt, medium_prompt, youtube_prompt, instagram_prompt
from tools.fetch_topics import fetch_topics
from datetime import datetime as dt
from utils.logger import log
import json

llm = get_ollama_model()

teacher_on_linkedin = create_agent(
    name="teacher_on_linkedin",
    model=llm,
    system_prompt=linkedin_prompt,
    tools=[fetch_topics],
    response_format=LinkedinResponse
)

teacher_on_instagram = create_agent(
    name="teacher_on_instagram",
    model=llm,
    system_prompt=instagram_prompt,
    tools=[fetch_topics],
    response_format=InstagramResponse
)

teacher_on_medium = create_agent(
    name="teacher_on_medium",
    model=llm,
    system_prompt=medium_prompt,
    tools=[fetch_topics],
    response_format=MediumResponse
)

teacher_on_youtube = create_agent(
    name="teacher_on_youtube",
    model=llm,
    system_prompt=youtube_prompt,
    tools=[fetch_topics],
    response_format=YoutubeResponse
)

class Teachers:
    def __init__(self):
        self.linkedin_teacher = teacher_on_linkedin
        self.instagram_teacher = teacher_on_instagram
        self.medium_teacher = teacher_on_medium
        self.youtube_teacher = teacher_on_youtube
        self.content = None
        self.date = dt.now().strftime("%Y%m%d")
        log("Teachers initialized")
    
    def run_teacher(self, teacher, retries=3):
        log(f"Running Agent: {teacher.name}")
        response = teacher.invoke({})
        if 'structured_response' in response:
            return response['structured_response']
        else:
            if retries > 0:
                log(f"Agent {teacher.name} failed. Retrying... ({3 - retries + 1}/3)")
                return self.run_teacher(teacher, retries - 1)
    
    def run(self) -> TeachersResponse:
        linkedin_response = self.run_teacher(self.linkedin_teacher)
        instagram_response = self.run_teacher(self.instagram_teacher)
        medium_response = self.run_teacher(self.medium_teacher)
        youtube_response = self.run_teacher(self.youtube_teacher)
    
        log("All Agents completed. Compiling results...")
        self.content = TeachersResponse(
            linkedin_post=linkedin_response,
            instagram_post=instagram_response,
            medium_post=medium_response,
            youtube_post=youtube_response
        )
        return self.content
        
    def save_content(self, filename: str = None):
        if not filename:
            filename = f"assets/output/teachers_{self.date}.json"
        json.dump(self.content.model_dump(), open(filename, 'w'))
            
# teachers = Teachers()
# teachers.run()
# teachers.save_content("agents/output/teachers_response.json")