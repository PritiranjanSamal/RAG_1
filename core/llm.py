import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from config import (
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

from core.prompts import SYSTEM_PROMPT

load_dotenv()


class GroqLLM:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY1"),
            model_name=LLM_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

    def generate_answer(
            self,
            question,
            context,
            history=""
    ):

        prompt = SYSTEM_PROMPT.format(
            history=history,
            context=context,
            question=question
        )

        response = self.llm.invoke(prompt)

        return response.content