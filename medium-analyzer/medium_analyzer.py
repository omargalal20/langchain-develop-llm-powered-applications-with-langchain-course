from langchain_aws import BedrockEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_pinecone import PineconeVectorStore
from loguru import logger
from pinecone import Pinecone

from clients.llm_client import LLMClient
from config.settings import get_settings


def retrieval(query: str, number_of_documents_to_retrieve: int, vector_store: VectorStore):
    logger.info("Retrieval")

    results = vector_store.similarity_search(
        query,
        k=number_of_documents_to_retrieve,
    )
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")

    return results


def generation(query: str, retriever: VectorStoreRetriever) -> str:
    logger.info("Generation")

    # Define the prompt template
    rag_prompt = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        
        Question: {input} 
        
        Context: {context} 
        
        Answer:
    """

    # Prepare template variables
    template_vars = {
        "input": query,
    }
    rag_template = PromptTemplate(
        input_variables=["input", "context"],
        template=rag_prompt,
    )

    return llm_client.generate_rag_chain_response(retriever, rag_template, template_vars)


if __name__ == "__main__":
    logger.info("Hello from medium-analyzer!")

    settings = get_settings()
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    embeddings_model = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         region_name=settings.AWS_REGION)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    vector_store: VectorStore = PineconeVectorStore(index_name=settings.PINECONE_INDEX_NAME, index=index,
                                                    embedding=embeddings_model)
    llm_client = LLMClient()
    retriever: VectorStoreRetriever = vector_store.as_retriever()

    query: str = "What is Pinecone in machine learning"
    number_of_documents_to_retrieve: int = 4

    # context = retrieval(query, number_of_documents_to_retrieve, vector_store)

    response = generation(query, retriever)

    logger.info(f"Response: {response}")
