from langchain_ollama import ChatOllama
from utils.logger import log

def get_ollama_model(model_name: str = "qwen3:latest") -> ChatOllama:
    log(f"Initializing Ollama model: {model_name}")
    llm = ChatOllama(model=model_name, num_ctx=131098)
    return llm