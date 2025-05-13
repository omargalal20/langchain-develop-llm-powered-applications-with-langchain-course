from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.exceptions import LangChainException
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from loguru import logger

from business.clients.llm_client import LLMClient


class OrchestratorService:
    """
    OrchestratorService responsible for connecting to the LLM.
    """

    def __init__(
            self,
            llm_client: LLMClient,
            retriever: VectorStoreRetriever
    ):
        """
        Initialize with injected service dependencies.
        """
        self.llm_client = llm_client
        self.llm = llm_client.get_llm()
        self.retriever: VectorStoreRetriever = retriever

    def response(self, query: str) -> str:

        rag_prompt = """
            You are a knowledgeable FHIR expert and assistant specializing in healthcare standards and protocols. 
            Your role is to assist healthcare professionals by providing accurate and concise answers based on the 
            provided FHIR context. If the answer is unclear or not present in the context, clearly state that you 
            don't know. Be professional, concise, and authoritative in your response.

            Question: {input}

            FHIR Context: {context}

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

        # Generate the response using LLM
        try:
            logger.info("Retrieval")

            combine_docs_chain = create_stuff_documents_chain(
                self.llm, rag_template
            )
            retrieval_chain = create_retrieval_chain(retriever=self.retriever, combine_docs_chain=combine_docs_chain)

            logger.info("Generation")

            response = retrieval_chain.invoke(input=template_vars)
            return response
        except LangChainException as e:
            logger.error(f"LLM failed to generate response: {str(e)}")
            raise RuntimeError("LLM failed to generate response.") from e
        except Exception as e:
            logger.error(f"Unexpected error occurred during generation: {e}")
            raise
