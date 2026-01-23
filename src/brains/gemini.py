from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_model(model_name: str = "gemini-2.5-flash") -> ChatGoogleGenerativeAI:
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    return llm