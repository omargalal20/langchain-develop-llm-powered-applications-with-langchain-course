from typing import List

from pydantic import BaseModel


class Document(BaseModel):
    id: str
    metadata: dict
    page_content: str


class Response(BaseModel):
    input: str
    context: List[Document]
    answer: str
