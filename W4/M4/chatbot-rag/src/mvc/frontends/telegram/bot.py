from typing import Optional

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_groq import ChatGroq
from telegram import Update
from telegram.ext import ContextTypes

from mvc.frontends.telegram.config import TELEGRAM_BOT_TOKEN
from mvc.model import Workflow


class Bot:
    def __init__(
        self,
        llm: ChatGroq,
        retriever: Optional[VectorStoreRetriever] = None,
    ) -> None:
        self.llm = llm
        self.retriever = retriever
        self.workflows_by_chat_id: dict[int, Workflow] = {}

    def get_bot_token(self) -> str:
        return TELEGRAM_BOT_TOKEN

    def get_or_create_workflow(self, chat_id: int) -> Workflow:
        workflow = self.workflows_by_chat_id.get(chat_id)
        if workflow is None:
            workflow = Workflow(llm=self.llm, retriever=self.retriever)
            self.workflows_by_chat_id[chat_id] = workflow
        return workflow

    def reset_chat(self, chat_id: int) -> None:
        self.workflows_by_chat_id[chat_id] = Workflow(
            llm=self.llm, retriever=self.retriever
        )

    async def on_update_received(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        if not update.message:
            return

        msg = update.message
        chat_id = msg.chat_id
        text = msg.text

        if not text:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please send text so I can respond.",
            )
            return

        if text.startswith("/"):
            if text == "/start":
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Hi! Paste your CV and I will rate it.",
                )
            elif text == "/reset":
                self.reset_chat(chat_id)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Conversation reset.",
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Unknown command. Try /start or /reset.",
                )
            return

        workflow = self.get_or_create_workflow(chat_id)
        chunks: list[str] = []
        async for chunk in workflow.astream(text):
            chunks.append(chunk)

        response = "".join(chunks).strip()
        if not response:
            response = "I could not generate a response."

        await context.bot.send_message(chat_id=chat_id, text=response)
