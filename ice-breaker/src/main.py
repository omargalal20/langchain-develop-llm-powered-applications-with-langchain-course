from langchain_core.exceptions import LangChainException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from loguru import logger

from clients.llm_client import LLMClient
from clients.scraper_client import ScraperClient
from utils import clean_markdown

llm_client = LLMClient()
scraper_client = ScraperClient()


def main():
    logger.info("Hello from ResearchGate Ice-Breaker!")

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
        scraped_information = scraper_client.scrape_research_gate_profile(
            "https://www.researchgate.net/profile/Atsunori-Kashiwagi-3?_sg=FJybbQK0-mm6yrxtVHN5nbhL8h1qUojyDdIt-xjmeR2H0xqpjHbgwN4HAhflngfMDCx0Vc5znnIOjwo&_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InNpZ251cCIsInBhZ2UiOiJfZGlyZWN0In19"
        )
        if not scraped_information:
            raise ValueError("No information was scraped. Ensure the profile URL is valid.")
    except Exception as e:
        logger.error(f"Failed to scrape ResearchGate profile: {e}")
        return

    cleaned_markdown = clean_markdown(scraped_information.markdown)
    scraped_metadata = scraped_information.metadata


    logger.info(f"Scraped Metadata: {scraped_metadata}")

    # Prepare template variables
    template_vars = {
        "information": cleaned_markdown
    }

    logger.info(f"Template Variables: {template_vars}")

    # Generate output using LLM
    try:
        llm = llm_client.get_llm()
        chain = prompt_template | llm | StrOutputParser()

        response = chain.invoke(template_vars)
        logger.info(f"Response: \n{response}")
    except LangChainException as e:
        logger.error(f"LLM failed to generate response: {str(e)}")
        raise RuntimeError("LLM failed to generate response.") from e
    except Exception as e:
        logger.error(f"Unexpected error occurred during generation: {e}")
        raise


if __name__ == "__main__":
    main()
