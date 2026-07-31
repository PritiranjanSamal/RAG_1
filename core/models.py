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