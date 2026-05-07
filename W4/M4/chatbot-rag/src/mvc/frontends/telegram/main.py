from telegram.ext import Application, MessageHandler, filters

from mvc.frontends.telegram.bot import Bot
from mvc.config import MODEL_NAME, GROQ_API_KEY, CHROMA_PATH, CHROMA_COLLECTION
from mvc.services.llm import new_llm
from mvc.services.db import ChromaDB
from mvc.services.embedding import new_embedding_function


def main():
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

    bot = Bot(llm=llm, retriever=db.as_retriever(k=4))

    application = Application.builder().token(bot.get_bot_token()).build()
    application.add_handler(MessageHandler(filters.ALL, bot.on_update_received))
    application.run_polling()


if __name__ == "__main__":
    main()
