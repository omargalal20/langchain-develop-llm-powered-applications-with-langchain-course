import os
from uuid import uuid4

from langchain.text_splitter import CharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore
from loguru import logger
from pinecone import Pinecone

from config.settings import get_settings


def ingestion(vector_store: VectorStore):
    logger.info("Indexing")

    # Load
    file_path = os.path.abspath("mediumblog1.txt")

    text_loader = TextLoader(

        file_path=file_path,
        encoding="utf-8"
    )

    loaded_documents: list[Document] = text_loader.load()

    logger.info(f"Documents: {loaded_documents}")

    # Split

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    splitted_documents = text_splitter.split_documents(loaded_documents)

    logger.info(f"Splitted Documents: {splitted_documents}")

    # Embed and Store

    logger.info(f"Storing Documents")

    uuids = [str(uuid4()) for _ in range(len(splitted_documents))]
    vector_store.add_documents(documents=splitted_documents, ids=uuids)

    logger.info("Finished")


if __name__ == '__main__':
    logger.info("Hello from ingestion!")

    settings = get_settings()
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    embeddings_model = BedrockEmbeddings(model_id=settings.EMBEDDING_MODEL_ID,
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                         region_name=settings.AWS_REGION)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    vector_store: VectorStore = PineconeVectorStore(index_name=settings.PINECONE_INDEX_NAME, index=index,
                                                    embedding=embeddings_model)

    ingestion(vector_store)
