from typing import Any, Dict, List, Union

from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish
from langchain.schema import LLMResult
from langchain_aws import ChatBedrockConverse
from langchain_core.exceptions import LangChainException
from langchain_core.prompts import PromptTemplate
from loguru import logger

from config.settings import get_settings

settings = get_settings()


class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("*********")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        print(f"***LLM Response:***\n{response.generations[0][0].text}")
        print("*********")


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
                stop_sequences=["\nObservation", "Observation"],
                callbacks=[AgentCallbackHandler()],
            )
        except Exception as e:
            logger.error(f"LLM failed to instantiate: {str(e)}")
            raise RuntimeError("LLM failed to instantiate.") from e

    def get_llm(self):
        """Return the configured LLM instance."""
        return self.llm

    def generate_response(self, prompt_template: PromptTemplate, template_vars: dict) -> Union[
        AgentAction, AgentFinish]:
        # Generate output using LLM
        try:
            chain = prompt_template | self.llm | ReActSingleInputOutputParser()
            response = chain.invoke(template_vars)
            return response
        except LangChainException as e:
            logger.error(f"LLM failed to generate response: {str(e)}")
            raise RuntimeError("LLM failed to generate response.") from e
        except Exception as e:
            logger.error(f"Unexpected error occurred during generation: {e}")
            raise
