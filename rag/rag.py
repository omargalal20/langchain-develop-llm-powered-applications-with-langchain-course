from langchain_aws import BedrockEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_community.vectorstores import FAISS
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


def predefined_rag_chain_generation(query: str, retriever: VectorStoreRetriever) -> str:
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

    return llm_client.generate_predefined_rag_chain_response(retriever, rag_template, template_vars)


def get_pinecone_retriever() -> VectorStoreRetriever:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    embeddings_model = BedrockEmbeddings(model_id=settings.EMBEDDING_MODEL_ID,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         region_name=settings.AWS_REGION)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    vector_store: VectorStore = PineconeVectorStore(index_name=settings.PINECONE_INDEX_NAME, index=index,
                                                    embedding=embeddings_model)
    retriever: VectorStoreRetriever = vector_store.as_retriever()

    return retriever


def get_faiss_retriever() -> VectorStoreRetriever:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    embeddings_model = BedrockEmbeddings(model_id=settings.EMBEDDING_MODEL_ID,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         region_name=settings.AWS_REGION)
    new_vectorstore = FAISS.load_local(
        "faiss_index", embeddings_model, allow_dangerous_deserialization=True
    )
    retriever: VectorStoreRetriever = new_vectorstore.as_retriever()

    return retriever


if __name__ == "__main__":
    logger.info("Hello from RAG!")

    settings = get_settings()
    llm_client = LLMClient()

    query: str = "What is Pinecone in machine learning"
    number_of_documents_to_retrieve: int = 4

    pinecone_retriever: VectorStoreRetriever = get_pinecone_retriever()

    text_rag_response = predefined_rag_chain_generation(query, pinecone_retriever)

    logger.info(f"Text RAG Response: {text_rag_response}")

    faiss_retriever = get_faiss_retriever()

    pdf_rag_response = predefined_rag_chain_generation(query, faiss_retriever)

    logger.info(f"PDF RAG Response: {pdf_rag_response}")
