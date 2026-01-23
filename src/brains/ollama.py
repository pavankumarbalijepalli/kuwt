from langchain_ollama import ChatOllama

def get_ollama_model(model_name: str = "qwen3:latest") -> ChatOllama:
    llm = ChatOllama(model=model_name)
    return llm