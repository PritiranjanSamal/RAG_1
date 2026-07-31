from core.embeddings import EmbeddingManager
from core.vector_store import VectorStore
from core.retriever import RAGRetriever
from core.llm import GroqLLM
from core.history import ChatHistory
from core.models import RAGResponse
from core.logger import logger


class RAGPipeline:

    def __init__(self):

        logger.info("Initializing RAG Pipeline...")

        self.embedding_manager = EmbeddingManager()

        self.vector_store = VectorStore()

        self.retriever = RAGRetriever(
            vector_store=self.vector_store,
            embedding_manager=self.embedding_manager
        )

        self.llm = GroqLLM()

        self.history = ChatHistory()

        logger.info("RAG Pipeline Ready.")

    def ask(self, question: str) -> RAGResponse:

        logger.info(f"Question : {question}")

        # Save user message
        self.history.add_user(question)

        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(question)

        if len(retrieved_docs) == 0:

            answer = "No relevant information found."

            self.history.add_assistant(answer)

            return RAGResponse(
                answer=answer,
                sources=[],
                context=""
            )

        # Build context
        context = self.retriever.build_context(
            retrieved_docs
        )

        # Add previous chat history
        conversation = self.history.get_history()

        final_context = f"""
Conversation History:

{conversation}

Retrieved Context:

{context}
"""

        # Generate response
        answer = self.llm.generate_answer(
            question=question,
            context=final_context
        )

        self.history.add_assistant(answer)

        logger.info("Answer generated successfully.")

        return RAGResponse(
            answer=answer,
            sources=retrieved_docs,
            context=context
        )


pipeline = RAGPipeline()














import chainlit as cl

from rag import pipeline


@cl.on_chat_start
async def start():

    await cl.Message(
        content="""
# 📚 Document RAG Assistant

Hello 👋

Ask any question regarding your uploaded documents.

I will search the Vector Database and answer using Groq.
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):

    user_question = message.content

    response = pipeline.ask(user_question)

    source_text = ""

    if response.sources:

        source_text = "\n\n### Sources\n"

        for i, doc in enumerate(response.sources, start=1):

            source = doc.metadata.get("source", "Unknown")

            page = doc.metadata.get("page", "-")

            score = round(doc.score, 3)

            source_text += (
                f"{i}. **{source}** | "
                f"Page: {page} | "
                f"Score: {score}\n"
            )

    await cl.Message(
        content=response.answer + source_text
    ).send()
















