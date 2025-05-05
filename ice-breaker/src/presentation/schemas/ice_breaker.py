from typing import List

from pydantic import BaseModel, Field


class IceBreakerRequest(BaseModel):
    name: str = Field(...)


class IceBreakerResponse(BaseModel):
    summary: str = Field(description="Summary of the person")
    research_gate_profile_url: str = Field(description="ResearchGate profile URL of the person")
    facts: List[str] = Field(description="Interesting facts about the person")
    topics_of_interest: List[str] = Field(
        description="Topics that may interest the person"
    )
    ice_breakers: List[str] = Field(
        description="Create ice breakers to open a conversation with the person"
    )
