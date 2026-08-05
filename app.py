import chainlit as cl
from rag import pipeline


@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
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
    try: 
        history = cl.user_session.get("history", [])
        response = pipeline.ask(question=message.content, history=history)
        history.append({"content": message.content, "role": "user"})
        history.append({"content": response.answer, "role": "assistant"})
        cl.user_session.set("history", history)
        await cl.Message(
            content=response.answer
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"Error: {e}"
        ).send()

    # response = pipeline.ask(message.content)
    # await cl.Message(
    #     content=response.answer
    # ).send()11111111

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
    # ).send()2222222222222