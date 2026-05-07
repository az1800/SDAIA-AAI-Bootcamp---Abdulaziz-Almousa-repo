import io
from typing import Optional

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_groq import ChatGroq


system_prompt = """\
You are an expert HR consultant and professional CV reviewer with deep knowledge of \
hiring standards across industries and regions.

When a user pastes their CV, retrieve and apply the relevant best practices from your \
knowledge base (general guidelines, regional conventions, language quality) and produce \
a structured review:

1. **Overall Score** — X / 100
2. **Readability** — Is it clear, scannable, and well-structured?
3. **Language Quality** — Are bullet points strong? Any weak phrases or missing quantification?
4. **Professionalism** — Tone, formatting, appropriate content for the target market
5. **Strengths** — What stands out positively
6. **Weaknesses** — What is missing, vague, or hurting the CV
7. **Hiring Recommendation** — Strong Yes / Yes / Maybe / No
8. **Top 3 Improvements** — Specific and actionable, referencing best practices

Be honest and direct. Do not flatter. If the CV is weak, say so and explain why with \
reference to specific best practices.\
"""

_rag_context_template = """\
The following best practices and guidelines were retrieved from the knowledge base. \
Use them to ground your CV review in concrete standards.

--- Retrieved guidelines ---
{context}
--- End of guidelines ---\
"""


class Workflow:
    def __init__(
        self,
        llm: ChatGroq,
        retriever: Optional[VectorStoreRetriever] = None,
    ) -> None:
        self.runnable = llm | StrOutputParser()
        self.retriever = retriever
        self.messages: list[BaseMessage] = [SystemMessage(system_prompt)]

    async def astream(self, message: str):
        prompt_messages: list[BaseMessage] = list(self.messages)

        if self.retriever is not None:
            docs = self.retriever.invoke(message)
            if docs:
                context_text = "\n\n".join(
                    f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
                    for doc in docs
                )
                prompt_messages.append(
                    SystemMessage(_rag_context_template.format(context=context_text))
                )

        prompt_messages.append(HumanMessage(message))

        chunks: list[str] = []
        async for chunk in self.runnable.astream(prompt_messages):
            chunks.append(chunk)
            yield chunk

        self.messages.append(HumanMessage(message))
        self.messages.append(AIMessage("".join(chunks)))

    def messages_to_markdown(self) -> str:
        text = io.StringIO()
        for msg in self.messages:
            if isinstance(msg, HumanMessage):
                who = "**👤 User**"
            elif isinstance(msg, AIMessage):
                who = "**🤖 Bot**"
            elif isinstance(msg, SystemMessage):
                who = "**💻️ System**"
            else:
                who = f"**{msg.type}**"
            text.write(f"{who}: {msg.content}\n\n")
        return text.getvalue()