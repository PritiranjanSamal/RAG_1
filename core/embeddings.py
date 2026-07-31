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