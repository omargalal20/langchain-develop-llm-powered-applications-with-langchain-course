from typing import Any, Dict, List

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.exceptions import LangChainException
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from loguru import logger

from business.clients.langsmith_client import LangSmithClient
from business.clients.llm_client import LLMClient
from business.schemas.llm import Response


class OrchestratorService:
    """
    OrchestratorService responsible for connecting to the LLM.
    """

    def __init__(
            self,
            llm_client: LLMClient,
            retriever: VectorStoreRetriever,
            langsmith_client: LangSmithClient,
    ):
        """
        Initialize with injected service dependencies.
        """
        self.llm_client = llm_client
        self.llm = llm_client.get_llm()
        self.retriever: VectorStoreRetriever = retriever
        self.chat_history_prompt = langsmith_client.get_prompt("langchain-ai/chat-langchain-rephrase")

    def response(self, query: str, chat_history: List[Dict[str, Any]]) -> Response:

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
            "chat_history": chat_history
        }
        rag_template = PromptTemplate(
            input_variables=["input", "context"],
            template=rag_prompt,
        )

        # Generate the response using LLM
        try:
            logger.info("Retrieval")
            history_aware_retriever = create_history_aware_retriever(
                llm=self.llm, retriever=self.retriever, prompt=self.chat_history_prompt
            )

            logger.info("Augmentation")
            combine_docs_chain = create_stuff_documents_chain(
                self.llm, rag_template
            )
            retrieval_chain = create_retrieval_chain(retriever=history_aware_retriever,
                                                     combine_docs_chain=combine_docs_chain)

            logger.info("Generation")
            response = retrieval_chain.invoke(input=template_vars)
            return Response(
                input=response["input"],
                answer=response["answer"],
                context=response["context"],
            )
        except LangChainException as e:
            logger.error(f"LLM failed to generate response: {str(e)}")
            raise RuntimeError("LLM failed to generate response.") from e
        except Exception as e:
            logger.error(f"Unexpected error occurred during generation: {e}")
            raise
