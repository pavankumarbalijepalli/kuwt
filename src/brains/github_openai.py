from langchain_openai import ChatOpenAI
import os


def get_github_model():
    llm = ChatOpenAI(
        model="gpt-4.1",
        base_url="https://models.github.ai/inference",
        api_key=os.getenv("GITHUB_TOKEN"),
    )
    return llm
