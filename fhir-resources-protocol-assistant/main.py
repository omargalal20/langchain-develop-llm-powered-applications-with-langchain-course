from langchain_aws import BedrockEmbeddings
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_pinecone import PineconeVectorStore
from loguru import logger
from pinecone import Pinecone

from business.clients.llm_client import LLMClient
from business.services.orchestrator_service import OrchestratorService
from config.settings import get_settings


def get_pinecone_retriever(NUMBER_OF_DOCUMENTS_TO_RETRIEVE: int) -> VectorStoreRetriever:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    embeddings_model = BedrockEmbeddings(model_id=settings.EMBEDDING_MODEL_ID,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         region_name=settings.AWS_REGION)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    vector_store: VectorStore = PineconeVectorStore(index_name=settings.PINECONE_INDEX_NAME, index=index,
                                                    embedding=embeddings_model)
    retriever: VectorStoreRetriever = vector_store.as_retriever(search_kwargs={"k": NUMBER_OF_DOCUMENTS_TO_RETRIEVE})

    return retriever


if __name__ == "__main__":
    NUMBER_OF_DOCUMENTS_TO_RETRIEVE: int = 10

    settings = get_settings()
    llm_client = LLMClient()
    pinecone_retriever: VectorStoreRetriever = get_pinecone_retriever(NUMBER_OF_DOCUMENTS_TO_RETRIEVE)
    service = OrchestratorService(llm_client=llm_client, retriever=pinecone_retriever)

    correct_query: str = "Give me a real test example of a MedicationRequest resource in FHIR?"
    response: str = service.response(query=correct_query)
    logger.info(f"Correct Query Response: {response}")

    wrong_query = "How many implementation guides are available for FHIR in the current version?"
    response: str = service.response(query=wrong_query)
    logger.info(f"Wrong Query Response: {response}")
