from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv

load_dotenv('D:\\kundelu-ai\\air-kuwt\\.env') 

def get_mistral_model(
    model_name: str = "mistral-large-latest"
) -> ChatMistralAI:
    llm = ChatMistralAI(
        model=model_name,
        temperature=0.3,
        streaming=True,
    )
    return llm