from langchain_google_genai import ChatGoogleGenerativeAI
import os


def get_gemini_model(
    user: str, model_name: str = "gemini-2.5-flash"
) -> ChatGoogleGenerativeAI:
    llm = ChatGoogleGenerativeAI(
        model=model_name, temperature=0, api_key=os.getenv(user)
    )
    return llm
