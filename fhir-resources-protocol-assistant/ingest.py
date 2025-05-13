from itertools import islice
from uuid import uuid4

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore
from loguru import logger
from pinecone import Pinecone

from config.settings import get_settings


def batch_iterator(iterable, batch_size):
    """
    Helper function to yield batches from an iterable.
    """
    iterator = iter(iterable)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch


def ingestion(vector_store: VectorStore):
    logger.info("Indexing")

    # Load
    logger.info(f"Loading Documents")

    loader = DirectoryLoader(path="scraped_data/fhir", glob="**/*.html", loader_cls=UnstructuredHTMLLoader)
    loaded_documents: list[Document] = loader.load()

    logger.info(f"Number of Documents: {len(loaded_documents)}")

    # Split

    logger.info(f"Splitting Documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,  # Maximum characters in each chunk
        chunk_overlap=200,  # Overlap to ensure context continuity
    )
    splitted_documents = splitter.split_documents(loaded_documents)

    for doc in splitted_documents:
        local_path = doc.metadata.get("source", "")
        if "scraped_data\\fhir\\" in local_path:  # Handle Windows-style paths
            # Transform local file path to actual FHIR URL
            relative_path = local_path.replace("scraped_data\\fhir\\", "").replace("\\", "/")
            fhir_url = f"https://hl7.org/fhir/R5/{relative_path}"
            doc.metadata.update({"source": fhir_url})
        else:
            logger.warning(f"Source path not in expected format: {local_path}")

    logger.info(f"Number of Splitted Documents: {len(splitted_documents)}")

    # Embed and Store Documents in Batches
    batch_size = 500
    logger.info(f"Embedding and Storing Documents in batches of {batch_size}")

    for i, batch in enumerate(batch_iterator(splitted_documents, batch_size)):
        uuids = [str(uuid4()) for _ in range(len(batch))]
        vector_store.add_documents(documents=batch, ids=uuids)
        logger.info(f"Processed batch {i + 1}")

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
