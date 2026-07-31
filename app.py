import chainlit as cl

from rag import pipeline


@cl.on_chat_start
async def start():

    await cl.Message(
        content="""
# 📚 Document RAG Assistant

Hello 👋

Welcome to the RAG Assistant.
\n\nAsk me about the documents that you have uploaded.
I will search the Vector Database and answer using Groq.
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):

    response = pipeline.ask(message.content)
    await cl.Message(
        content=response.answer
    ).send()

    # user_question = message.content

    # response = pipeline.ask(user_question)

    # source_text = ""

    # if response.sources:

    #     source_text = "\n\n### Sources\n"

    #     for i, doc in enumerate(response.sources, start=1):

    #         source = doc.metadata.get("source", "Unknown")

    #         page = doc.metadata.get("page", "-")

    #         score = round(doc.score, 3)

    #         source_text += (
    #             f"{i}. **{source}** | "
    #             f"Page: {page} | "
    #             f"Score: {score}\n"
    #         )

    # await cl.Message(
    #     content=response.answer + source_text
    # ).send()