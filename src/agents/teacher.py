from langchain.agents import create_agent
from brains.ollama import get_ollama_model
from models.fundamentals import LinkedinResponse
from prompts.fundamentals import linkedin_prompt, medium_prompt, youtube_prompt, instagram_prompt
from tools.fetch_topics import fetch_topics

llm = get_ollama_model("qwen3:latest")

teacher_on_linkedin = create_agent(
    name="teacher_on_linkedin",
    model=llm,
    system_prompt=linkedin_prompt,
    tools=[fetch_topics],
    response_format=LinkedinResponse
)

response = teacher_on_linkedin.invoke(input={})