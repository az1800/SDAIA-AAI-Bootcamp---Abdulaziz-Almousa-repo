import chainlit as cl

from mvc.config import GROQ_API_KEY, MODEL_NAME, CHROMA_PATH, CHROMA_COLLECTION
from mvc.model import Workflow
from mvc.services.llm import new_llm
from mvc.services.db import ChromaDB
from mvc.services.embedding import new_embedding_function


# Build the DB singleton once at module load (shared across all sessions).
_db = ChromaDB(
    path=CHROMA_PATH,
    collection=CHROMA_COLLECTION,
    embedding_function=new_embedding_function(),
)


@cl.on_chat_start
async def on_chat_start():
    llm = new_llm(
        model=MODEL_NAME,
        groq_api_key=GROQ_API_KEY,
        streaming=True,
    )
    workflow = Workflow(llm=llm, retriever=_db.as_retriever(k=4))
    cl.user_session.set("workflow", workflow)


@cl.on_message
async def on_message(message: cl.Message):
    workflow: Workflow = cl.user_session.get("workflow")
    msg = cl.Message(content="")
    async for chunk in workflow.astream(message.content):
        await msg.stream_token(chunk)
    await msg.send()
