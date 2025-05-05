from typing import Annotated

from fastapi import Depends

from business.agents.research_gate_lookup_agent import ResearchGateLookupAgent
from business.clients.langsmith_client import LangSmithClient
from business.clients.llm_client import LLMClient
from business.clients.scraper_client import ScraperClient


def get_llm_client() -> LLMClient:
    return LLMClient()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]


def get_scraper_client() -> ScraperClient:
    return ScraperClient()


ScraperClientDependency = Annotated[ScraperClient, Depends(get_scraper_client)]


def get_langsmith_client() -> LangSmithClient:
    return LangSmithClient()


LangSmithClientDependency = Annotated[LangSmithClient, Depends(get_langsmith_client)]


def get_research_gate_lookup_agent(
        llm_client: LLMClientDependency,
        langsmith_client: LangSmithClientDependency) -> ResearchGateLookupAgent:
    return ResearchGateLookupAgent(llm_client, langsmith_client)


ResearchGateLookupAgentDependency = Annotated[ResearchGateLookupAgent, Depends(get_research_gate_lookup_agent)]
