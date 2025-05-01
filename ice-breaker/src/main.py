from langchain_core.exceptions import LangChainException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from loguru import logger

from clients.llm_client import LLMClient

llm_client = LLMClient()


def main():
    logger.info("Hello from ice-breaker!")

    prompt_template = PromptTemplate(
        input_variables=["topic"],
        template="""Tell me a joke about {topic}"""
    )

    template_vars = {
        "topic": "cats"
    }

    logger.debug(f"Medical QA Template Variables: {template_vars}")

    llm = llm_client.get_llm()

    # Generation
    chain = prompt_template | llm | StrOutputParser()

    try:
        response = chain.invoke(template_vars)

        logger.debug(f"Response: \n{response}")
    except LangChainException as e:
        logger.error(f"LLM failed to generate response: {str(e)}")
        raise RuntimeError("LLM failed to generate response.") from e


if __name__ == "__main__":
    main()
