import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Paths
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VECTOR_STORE_PATH = os.path.join(
    BASE_DIR,
    "Data",
    "Vector_Store"
)

PDF_DIRECTORY = os.path.join(
    BASE_DIR,
    "Data",
    "PDF"
)

COLLECTION_NAME = "pdf_documents"

# -------------------------
# Embedding Model
# -------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# -------------------------
# Groq
# -------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = "llama-3.1-8b-instant"

TEMPERATURE = 0.1

MAX_TOKENS = 1024

# -------------------------

TOP_K = 5

MIN_SCORE = 0.20









from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingManager:

    def __init__(self,
                 model_name=EMBEDDING_MODEL):

        self.model_name = model_name

        self.model = SentenceTransformer(
            self.model_name
        )

    def generate_embeddings(
            self,
            texts: List[str]
    ) -> np.ndarray:

        if len(texts) == 0:
            return np.array([])

        embeddings = self.model.encode(
            texts,
            show_progress_bar=False
        )

        return embeddings

    @property
    def dimension(self):

        return self.model.get_sentence_embedding_dimension()







import uuid
import chromadb

from config import (
    VECTOR_STORE_PATH,
    COLLECTION_NAME
)


class VectorStore:

    def __init__(
            self,
            collection_name=COLLECTION_NAME,
            persist_directory=VECTOR_STORE_PATH
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description":
                "PDF document embeddings"
            }
        )

    def add_documents(
            self,
            documents,
            embeddings
    ):

        ids = []

        docs = []

        metas = []

        vectors = []

        for i, (doc, emb) in enumerate(
                zip(documents, embeddings)
        ):

            ids.append(
                f"doc_{uuid.uuid4().hex}"
            )

            docs.append(
                doc.page_content
            )

            metadata = dict(doc.metadata)

            metadata["doc_index"] = i

            metadata["content_length"] = len(
                doc.page_content
            )

            metas.append(metadata)

            vectors.append(
                emb.tolist()
            )

        self.collection.add(

            ids=ids,

            documents=docs,

            metadatas=metas,

            embeddings=vectors

        )

    def count(self):

        return self.collection.count()









from dataclasses import dataclass
from typing import List

from config import TOP_K


@dataclass
class RetrievedDocument:
    content: str
    metadata: dict
    score: float


class RAGRetriever:

    def __init__(
        self,
        vector_store,
        embedding_manager
    ):

        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K
    ) -> List[RetrievedDocument]:

        # Generate embedding for user query
        query_embedding = self.embedding_manager.generate_embeddings(
            [query]
        )[0]

        # Search ChromaDB
        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        retrieved_docs = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            score = 1 - float(distance)

            retrieved_docs.append(

                RetrievedDocument(

                    content=document,

                    metadata=metadata,

                    score=score

                )

            )

        return retrieved_docs

    def build_context(
        self,
        documents: List[RetrievedDocument]
    ) -> str:

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += f"""
============= Document {i} =============

Source:
{doc.metadata.get("source", "Unknown")}

Page:
{doc.metadata.get("page", "Unknown")}

Content:

{doc.content}


"""

        return context.strip()









SYSTEM_PROMPT = """
You are an intelligent AI assistant.

You must answer ONLY from the supplied context.

If the answer is not present in the context, simply say:

"I couldn't find this information in the uploaded documents."

Never make up facts.

----------------------------------------
Context
----------------------------------------

{context}

----------------------------------------
Question
----------------------------------------

{question}

----------------------------------------
Answer
----------------------------------------
"""












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

            groq_api_key=os.getenv("GROQ_API_KEY"),

            model_name=LLM_MODEL,

            temperature=TEMPERATURE,

            max_tokens=MAX_TOKENS

        )

    def generate_answer(

            self,

            question,

            context

    ):

        prompt = SYSTEM_PROMPT.format(

            context=context,

            question=question

        )

        response = self.llm.invoke(prompt)

        return response.content













