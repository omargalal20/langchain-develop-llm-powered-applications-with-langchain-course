from firecrawl import FirecrawlApp
from firecrawl.firecrawl import ScrapeResponse
from loguru import logger
from requests.exceptions import HTTPError

from config.settings import get_settings

settings = get_settings()


class ScraperClient:
    """
    Scraper Client
    """

    def __init__(self):
        """
        Initialize Scraper configuration.
        """
        self.scraper_client = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)

    def scrape_research_gate_profile(self, profile_url: str) -> ScrapeResponse:
        """
        Scrape information from ResearchGate profile,
        Manually scrape the information from the ResearchGate profile
        """
        logger.info(f"Attempting to scrape ResearchGate profile: {profile_url}")
        try:
            scraped_linkedin_profile: ScrapeResponse = self.scraper_client.scrape_url(
                url=profile_url, formats=['markdown']
            )
            # I need Name, Skills and Expertise, Publications
            return scraped_linkedin_profile
        except HTTPError as e:
            logger.error(f"HTTPError occurred while scraping: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
