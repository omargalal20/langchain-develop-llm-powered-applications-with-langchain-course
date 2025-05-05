from typing import Annotated

from fastapi import Depends

from business.dependencies import (
    LLMClientDependency,
    ScraperClientDependency,
    LangSmithClientDependency,
    ResearchGateLookupAgentDependency,
)
from business.services.orchestrator_service import OrchestratorService


def get_orchestrator(
        llm_client: LLMClientDependency,
        scraper_client: ScraperClientDependency,
        langsmith_client: LangSmithClientDependency,
        research_gate_lookup_agent: ResearchGateLookupAgentDependency,
) -> OrchestratorService:
    """Provide a configured OrchestratorService."""
    return OrchestratorService(
        llm_client=llm_client,
        scraper_client=scraper_client,
        langsmith_client=langsmith_client,
        research_gate_lookup_agent=research_gate_lookup_agent,
    )


OrchestratorServiceDependency = Annotated[OrchestratorService, Depends(get_orchestrator)]
