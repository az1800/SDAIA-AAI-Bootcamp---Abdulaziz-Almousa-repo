from langchain_groq import ChatGroq


def new_llm(model: str, groq_api_key: str, streaming: bool = False):
    return ChatGroq(
        model=model,
        temperature=0,
        api_key=groq_api_key,
        streaming=streaming,
    )
