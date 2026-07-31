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