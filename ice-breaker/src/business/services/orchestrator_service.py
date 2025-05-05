from firecrawl.firecrawl import ScrapeResponse
from langchain_core.prompts import PromptTemplate
from loguru import logger

from business.agents.research_gate_lookup_agent import ResearchGateLookupAgent
from business.clients.langsmith_client import LangSmithClient
from business.clients.llm_client import LLMClient
from business.clients.scraper_client import ScraperClient
from business.output_parsers.ice_breaker import summary_parser, Summary
from presentation.schemas.ice_breaker import IceBreakerResponse
from utils import clean_markdown


class OrchestratorService:
    """
    OrchestratorService responsible for connecting the LLM to external services and providing enhanced capabilities.
    """

    def __init__(
            self,
            llm_client: LLMClient,
            scraper_client: ScraperClient,
            langsmith_client: LangSmithClient,
            research_gate_lookup_agent: ResearchGateLookupAgent,
    ):
        """
        Initialize with injected service dependencies.
        """
        self.llm_client = llm_client
        self.scraper_client = scraper_client
        self.langsmith_client = langsmith_client
        self.research_gate_lookup_agent = research_gate_lookup_agent

    def ice_break_with(self, name: str) -> IceBreakerResponse:
        """
        Generate a personalized icebreaker for a researcher based on their ResearchGate profile.

        Parameters:
        - name (str): Full name of the researcher.

        Returns:
        - Summary: Contains the researcher's summary and two personalized icebreakers.

        Raises:
        - ValueError: If no information is retrieved from ResearchGate.
        """
        logger.info("Hello from ResearchGate Ice-Breaker!")

        # Lookup ResearchGate profile
        try:
            research_gate_profile_url = self.research_gate_lookup_agent.lookup(f"{name} ResearchGate")
        except Exception as e:
            logger.error(f"Error during ResearchGate lookup: {e}")
            raise

        logger.info(f"ResearchGate profile URL: {research_gate_profile_url}")

        if not research_gate_profile_url:
            raise ValueError("Failed to retrieve the ResearchGate profile URL.")

        # Scrape profile information
        try:
            scraped_information: ScrapeResponse = self.scraper_client.scrape_research_gate_profile(
                research_gate_profile_url)
            if not scraped_information:
                raise ValueError("No information was scraped. Ensure the profile URL is valid.")
        except Exception as e:
            logger.error(f"Failed to scrape ResearchGate profile: {e}")
            raise ValueError("Error scraping ResearchGate profile.") from e

        cleaned_markdown = clean_markdown(scraped_information.markdown)

        # Define the prompt template
        summary_template = """
            Given the following ResearchGate information about a researcher:
            {information}

            Create:
            1. A concise summary of their professional focus and contributions.
            2. Two interesting facts about them.
            3. A topic that may interest them.
            4. Two personalized ice breakers for starting a conversation, focusing on their research or interests.

            Output Format:
            \n{format_instructions}
        """
        prompt_template = PromptTemplate(
            input_variables=["information"],
            template=summary_template,
            partial_variables={"format_instructions": summary_parser.get_format_instructions()},
        )

        # Prepare template variables
        template_vars = {
            "information": cleaned_markdown,
        }

        # Generate the response using LLM
        try:
            response: Summary = self.llm_client.generate_response(prompt_template, template_vars)
            logger.info(f"Generated response: {response}")
            return IceBreakerResponse(
                summary=response.summary,
                research_gate_profile_url=research_gate_profile_url,
                facts=response.facts,
                topics_of_interest=response.topics_of_interest,
                ice_breakers=response.ice_breakers
            )
        except Exception as e:
            logger.error(f"Failed to generate ice breaker response: {e}")
            raise RuntimeError("Failed to generate ice breaker response.") from e
