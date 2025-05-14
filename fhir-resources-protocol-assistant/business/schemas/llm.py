from typing import List

from langchain_core.documents import Document
from pydantic import BaseModel


class Response(BaseModel):
    input: str
    context: List[Document]
    answer: str
