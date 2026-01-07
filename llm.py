from langchain_google_genai import ChatGoogleGenerativeAI

def create_chat():
    return ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

