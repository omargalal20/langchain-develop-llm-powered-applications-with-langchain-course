from firecrawl.firecrawl import ScrapeResponse
from langchain_core.prompts import PromptTemplate
from loguru import logger

from agents.research_gate_lookup_agent import ResearchGateLookupAgent
from clients.langsmith_client import LangSmithClient
from clients.llm_client import LLMClient
from clients.scraper_client import ScraperClient
from utils import clean_markdown


def ice_break_with(name: str) -> str:
    logger.info("Hello from ResearchGate Ice-Breaker!")

    research_gate_profile_url = research_gate_lookup_agent.lookup(f"{name} ResearchGate")

    logger.info(f"research_gate_profile_url: {research_gate_profile_url}")

    # Define the prompt template
    summary_template = """
        Given the following ResearchGate information about a healthcare professional:
        {information}

        Create:
        1. A concise summary of their professional focus and contributions.
        2. Two personalized ice breakers for starting a conversation, focusing on their research or interests.
    """

    prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template
    )

    # Scrape information
    try:
        scraped_information: ScrapeResponse = scraper_client.scrape_research_gate_profile(research_gate_profile_url)
        if not scraped_information:
            raise ValueError("No information was scraped. Ensure the profile URL is valid.")
    except Exception as e:
        logger.error(f"Failed to scrape ResearchGate profile: {e}")

    cleaned_markdown = clean_markdown(scraped_information.markdown)

    # Prepare template variables
    template_vars = {
        "information": cleaned_markdown
    }

    response = llm_client.generate_response(prompt_template, template_vars)

    return response


if __name__ == "__main__":
    llm_client = LLMClient()
    scraper_client = ScraperClient()
    langsmith_client = LangSmithClient()
    research_gate_lookup_agent = ResearchGateLookupAgent()

    ice_breaker = ice_break_with("Yasser Shoukry")

    logger.info(f"Response: \n{ice_breaker}")
