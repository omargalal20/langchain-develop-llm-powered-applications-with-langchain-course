from typing import List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="Summary")
    ice_breakers: List[str] = Field(description="Ice breakers to ask them")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "ice_breakers": self.ice_breakers}


summary_parser = PydanticOutputParser(pydantic_object=Summary)