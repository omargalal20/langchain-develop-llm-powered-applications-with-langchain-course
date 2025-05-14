from typing import Set

import streamlit as st
from langchain_core.vectorstores import VectorStoreRetriever
from loguru import logger

from business.clients.langsmith_client import LangSmithClient
from business.clients.llm_client import LLMClient
from business.clients.vector_store_client import VectorStoreClient
from business.schemas.llm import Response
from business.services.orchestrator_service import OrchestratorService
from config.settings import get_settings

# Initialize settings and services
settings = get_settings()
llm_client = LLMClient()
vector_store_client = VectorStoreClient()
langsmith_client = LangSmithClient()

retriever: VectorStoreRetriever = vector_store_client.get_retriever(
    settings.VECTOR_STORE_NUMBER_OF_DOCUMENTS_TO_RETRIEVE)
service = OrchestratorService(llm_client=llm_client, retriever=retriever, langsmith_client=langsmith_client)


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"- {source}\n"
    return sources_string


# Sidebar
with st.sidebar:
    st.markdown("# 🏥 About")
    st.markdown("""
    ### FHIR Resources Protocol Assistant
    
    This AI assistant helps you understand and work with FHIR (Fast Healthcare Interoperability Resources) protocols and standards. 
    
    **Features:**
    - Ask questions about FHIR resources
    - Get explanations of FHIR protocols
    - Access relevant documentation sources
    
    Built with:
    - Streamlit
    - LangChain
    - Pinecone
    - AWS Bedrock
    """)

# Main content
st.header("🏥 LangChain Udemy Course - FHIR Resources Protocol Assistant")

# Initialize session state for prompts and responses if not already done
if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Input prompt
prompt = st.chat_input("Enter your prompt here..")


logger.info(f"Prompt: {prompt}")

if prompt:
    with st.spinner("Generating response.."):
        response: Response = service.response(query=prompt, chat_history=st.session_state["chat_history"])

        sources = set(
            [doc.metadata["source"] for doc in response.context]
        )

        formatted_response = (
            f"{response.answer} \n\n {create_sources_string(sources)}"
        )

        logger.info(f"AI Response: {response.answer}")

        # Save prompt and response to session state
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", response.answer))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)
