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