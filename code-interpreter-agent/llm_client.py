from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from loguru import logger

from settings import get_settings

settings = get_settings()
load_dotenv()


class LLMClient:
    """LLM Client"""

    def __init__(self):
        """Initialize LLM configuration."""
        try:
            self.llm = ChatBedrockConverse(
                model_id=settings.MODEL_ID,
                temperature=settings.MODEL_TEMPERATURE,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
        except Exception as e:
            logger.error(f"LLM failed to instantiate: {str(e)}")
            raise RuntimeError("LLM failed to instantiate.") from e

    def get_llm(self):
        """Return the configured LLM instance."""
        return self.llm
