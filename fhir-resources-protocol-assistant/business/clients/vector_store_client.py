from langchain_aws import BedrockEmbeddings
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_pinecone import PineconeVectorStore
from loguru import logger
from pinecone import Pinecone

from config.settings import get_settings

settings = get_settings()


class VectorStoreClient:
    """VectorStoreClient"""

    def __init__(self):
        """Initialize VectorStoreClient configuration."""
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.embeddings_model = BedrockEmbeddings(model_id=settings.EMBEDDING_MODEL_ID,
                                                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                                      region_name=settings.AWS_REGION)
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            self.vector_store: VectorStore = PineconeVectorStore(index_name=settings.PINECONE_INDEX_NAME,
                                                                 index=self.index,
                                                                 embedding=self.embeddings_model)
        except Exception as e:
            logger.error(f"Vector Store failed to instantiate: {str(e)}")
            raise RuntimeError("Vector Store failed to instantiate.") from e

    def get_retriever(self, number_of_documents_to_retrieve: int) -> VectorStoreRetriever:
        """Return the configured retriever instance."""
        return self.vector_store.as_retriever(search_kwargs={"k": number_of_documents_to_retrieve})
