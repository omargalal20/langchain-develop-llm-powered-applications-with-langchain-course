from typing import Set

import streamlit as st
from langchain_core.vectorstores import VectorStoreRetriever
from loguru import logger

from business.clients.llm_client import LLMClient
from business.clients.vector_store_client import VectorStoreClient
from business.schemas.llm import Response
from business.services.orchestrator_service import OrchestratorService
from config.settings import get_settings

# Initialize settings and services
settings = get_settings()
llm_client = LLMClient()
vector_store_client = VectorStoreClient()

retriever: VectorStoreRetriever = vector_store_client.get_retriever(
    settings.VECTOR_STORE_NUMBER_OF_DOCUMENTS_TO_RETRIEVE)
service = OrchestratorService(llm_client=llm_client, retriever=retriever)


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"- {source}\n"
    return sources_string


# Streamlit app
st.header("LangChain Udemy Course - Documentation Helper Bot")

# Initialize session state for prompts and responses if not already done
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

# Input prompt
prompt = st.text_input("Prompt", placeholder="Enter your prompt here..")

logger.info(f"Prompt: {prompt}")

if prompt:
    with st.spinner("Generating response.."):
        response: Response = service.response(query=prompt)

        logger.info(f"Response: {response.answer}")

        sources = set(
            [doc.metadata["source"] for doc in response.context]
        )

        formatted_response = (
            f"{response.answer} \n\n {create_sources_string(sources)}"
        )

        # Save prompt and response to session state
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)
