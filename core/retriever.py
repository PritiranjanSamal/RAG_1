from dataclasses import dataclass
from typing import List

from config import TOP_K
from core.logger import logger


@dataclass
class RetrievedDocument:
    content: str
    metadata: dict
    score: float
    distance: float


class RAGRetriever:
    """Handles query-based retrieval from the vector store"""

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
        """
        Retrieve relevant documents for a query

        Args:
            query: Search query
            top_k: Number of documents to retrieve

        Returns:
            List of retrieved documents
        """
        logger.info(f"Retrieving documents for query: '{query}'")
        logger.info(f"Top K: {top_k}")

        try:
            # Generate query embedding
            query_embedding = self.embedding_manager.generate_embeddings([query])[0]

            # Query ChromaDB
            results = self.vector_store.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )

            retrieved_docs = []

            if results["documents"] and len(results["documents"][0]) > 0:

                documents = results["documents"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]
                ids = results.get("ids", [[]])[0]

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
                            score=score,
                            distance=float(distance)
                        )
                    )

                    logger.info(f"Distance: {distance:.4f} | Score: {score:.4f}")

                logger.info(f"Retrieved {len(retrieved_docs)} documents")

            else:
                logger.warning("No documents found")

            return retrieved_docs

        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []

    def build_context(
        self,
        documents: List[RetrievedDocument]
    ) -> str:
        """Build context string from retrieved documents"""
        # Simple format matching the working notebook approach
        return "\n\n".join([doc.content for doc in documents])