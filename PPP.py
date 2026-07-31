from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RetrievedDocument:
    content: str
    metadata: Dict
    score: float


@dataclass
class RAGResponse:
    answer: str
    sources: List[RetrievedDocument]
    context: str










from collections import deque


class ChatHistory:

    def __init__(self, max_messages=10):

        self.history = deque(maxlen=max_messages)

    def add_user(self, message):

        self.history.append(
            ("User", message)
        )

    def add_assistant(self, message):

        self.history.append(
            ("Assistant", message)
        )

    def get_history(self):

        history = ""

        for role, msg in self.history:

            history += f"{role}: {msg}\n"

        return history














import logging

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger("RAG")













class VectorStoreError(Exception):
    pass


class EmbeddingError(Exception):
    pass


class RetrievalError(Exception):
    pass


class LLMError(Exception):
    pass



















