import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from loguru import logger

from config.settings import get_settings


def ingestion():
    logger.info("Indexing")

    # Load

    folder_path = os.path.abspath("research_papers")

    pdf_loader = PyPDFDirectoryLoader(folder_path)

    loaded_documents: list[Document] = pdf_loader.load()

    logger.info(f"Documents: {loaded_documents}")

    # Split

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n"],
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )

    splitted_documents = text_splitter.split_documents(loaded_documents)

    logger.info(f"Splitted Documents: {splitted_documents}")

    # Embed and Store

    logger.info(f"Embedding and Storing Documents")

    embeddings_model = BedrockEmbeddings(model_id=settings.EMBEDDING_MODEL_ID,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         region_name=settings.AWS_REGION)

    vectorstore = FAISS.from_documents(splitted_documents, embeddings_model)
    vectorstore.save_local("faiss_index")

    logger.info("Finished")


if __name__ == '__main__':
    logger.info("Hello from ingestion!")

    settings = get_settings()

    ingestion()
