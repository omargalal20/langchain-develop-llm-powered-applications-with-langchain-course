from langchain.prompts import Prompt
from langsmith import Client
from loguru import logger
from requests.exceptions import HTTPError

from config.settings import get_settings

settings = get_settings()


class LangSmithClient:
    """
    LangSmith Client
    """

    def __init__(self):
        """
        Initialize LangSmith configuration.
        """
        self.langsmith_client = Client(api_key=settings.LANGSMITH_API_KEY)

    def get_prompt(self, prompt_name: str) -> Prompt:
        """
        Retrieve a stored prompt by name from LangSmith.

        :param prompt_name: The name of the prompt to retrieve.
        :return: A LangChain Prompt object.
        """
        logger.info(f"Fetching prompt with name: {prompt_name}")
        try:
            prompt = self.langsmith_client.pull_prompt(prompt_name, include_model=True)
            if not prompt:
                logger.warning(f"Prompt with name '{prompt_name}' not found.")

            logger.info(f"Successfully fetched prompt: {prompt_name}")
            return prompt
        except HTTPError as e:
            logger.error(f"HTTPError occurred while fetching prompt: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
