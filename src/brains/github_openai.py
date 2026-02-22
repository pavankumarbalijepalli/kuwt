from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv('/home/kundelu-ai/kundelu-ai/air-kai-content/.env')

def get_github_model():
     llm = ChatOpenAI(
        model="gpt-4.1",
        base_url="https://models.github.ai/inference",
        api_key=os.getenv("GITHUB_TOKEN"),
    )
     return llm