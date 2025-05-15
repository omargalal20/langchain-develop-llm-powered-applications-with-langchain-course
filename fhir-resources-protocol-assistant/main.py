from langchain_core.vectorstores import VectorStoreRetriever
from loguru import logger

from business.clients.langsmith_client import LangSmithClient
from business.clients.llm_client import LLMClient
from business.clients.vector_store_client import VectorStoreClient
from business.schemas.llm import Response
from business.services.orchestrator_service import OrchestratorService
from config.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    llm_client = LLMClient()
    vector_store_client = VectorStoreClient()
    langsmith_client = LangSmithClient()

    retriever: VectorStoreRetriever = vector_store_client.get_retriever(
        settings.VECTOR_STORE_NUMBER_OF_DOCUMENTS_TO_RETRIEVE)
    service = OrchestratorService(llm_client=llm_client, retriever=retriever, langsmith_client=langsmith_client)

    correct_query: str = "Give me a real test example of a MedicationRequest resource in FHIR?"
    response: Response = service.response(query=correct_query, chat_history=[])
    logger.info(f"Correct Query Response: {response.answer}")

    wrong_query = "How many implementation guides are available for FHIR in the current version?"
    response: Response = service.response(query=wrong_query, chat_history=[])
    logger.info(f"Wrong Query Response: {response.answer}")
