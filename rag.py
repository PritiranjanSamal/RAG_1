from core.embeddings import EmbeddingManager
from core.vector_store import VectorStore
from core.retriever import RAGRetriever
from core.llm import GroqLLM
from core.models import RAGResponse
from core.logger import logger
from config import TOP_K


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

        logger.info("RAG Pipeline Ready.")

    def ask(self, question: str, top_k: int = TOP_K, min_score: float = 0.05, history=None) -> RAGResponse:
        """
        Ask a question using the RAG pipeline
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            min_score: Minimum relevance score threshold (0-1, lower distance = higher score)
            history: Optional conversation history
            
        Returns:
            RAGResponse with answer, sources, and context
        """
        logger.info(f"Question: {question}")
        logger.info(f"Using top_k={top_k}, min_score={min_score}")

        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)

        if not retrieved_docs:
            logger.warning("No documents retrieved")
            return RAGResponse(
                answer="No relevant information found.",
                sources=[],
                context=""
            )

        # Filter by minimum score (distance-based: lower distance = higher similarity)
        filtered_docs = [doc for doc in retrieved_docs if doc.score >= min_score]
        
        if not filtered_docs:
            logger.warning(f"No documents met minimum score threshold of {min_score}")
            logger.info(f"Retrieved scores: {[doc.score for doc in retrieved_docs]}")
            return RAGResponse(
                answer="No relevant information found meeting the minimum score threshold.",
                sources=[],
                context=""
            )

        logger.info(f"Using {len(filtered_docs)} documents after filtering (from {len(retrieved_docs)} retrieved)")

        # Build context from filtered documents
        context = self.retriever.build_context(filtered_docs)

        # Add previous chat history
        conversation_history = ""

        if history:
            for msg in history:
                role = msg.get("role", "").lower()

                if role == "user":
                    conversation_history += f"User: {msg.get('content', '')}\n"

                elif role == "assistant":
                    conversation_history += f"Assistant: {msg.get('content', '')}\n"

        # Generate response
        answer = self.llm.generate_answer(
            question=question,
            context=context,
            history=conversation_history
        )

        logger.info("Answer generated successfully.")

        # Calculate confidence (max score from filtered docs)
        confidence = max([doc.score for doc in filtered_docs])
        logger.info(f"Confidence: {confidence:.4f}")

        return RAGResponse(
            answer=answer,
            sources=filtered_docs,
            context=context
        )


pipeline = RAGPipeline()