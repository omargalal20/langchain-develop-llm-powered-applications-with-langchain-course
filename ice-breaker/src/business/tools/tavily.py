from typing import List

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from pydantic import BaseModel

from config.settings import get_settings

settings = get_settings()


class ResearchGateProfile(BaseModel):
    title: str
    url: str
    score: float


@tool("get_research_gate_profile_urls", parse_docstring=True)
def get_profile_urls_tavily(name: str) -> List[ResearchGateProfile]:
    """Searches for ResearchGate Profile Pages.

    Args:
        name: The name of the researcher to search for.

    Returns:
        A list of Pydantic objects containing {
            title: str,
            url: str,
            score: float
        }.
    """
    search = TavilySearch(
        tavily_api_key=settings.TAVILY_API_KEY,
    )
    response = search.invoke(f"{name}")
    results = response["results"]

    def map_result(result: dict) -> ResearchGateProfile:
        return ResearchGateProfile(
            title=result["title"],
            url=result["url"],
            score=result["score"]
        )

    return [map_result(result) for result in results]
