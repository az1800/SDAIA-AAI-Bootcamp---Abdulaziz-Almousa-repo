from mvc.model import Workflow
from mvc.frontends.cli.view import SupportBotApp
from mvc.services.llm import new_llm
from mvc.services.db import ChromaDB
from mvc.services.embedding import new_embedding_function
from mvc.config import MODEL_NAME, GROQ_API_KEY, CHROMA_PATH, CHROMA_COLLECTION

if __name__ == "__main__":
    llm = new_llm(
        model=MODEL_NAME,
        groq_api_key=GROQ_API_KEY,
        streaming=True,
    )

    db = ChromaDB(
        path=CHROMA_PATH,
        collection=CHROMA_COLLECTION,
        embedding_function=new_embedding_function(),
    )

    workflow = Workflow(llm=llm, retriever=db.as_retriever(k=4))
    app = SupportBotApp(workflow=workflow)
    app.run()