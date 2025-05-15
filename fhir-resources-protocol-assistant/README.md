# FHIR Resources Protocol Assistant

This application helps healthcare professionals quickly access relevant information about FHIR, specifically FHIR
resources and how they are constructed. It draws from the FHIR Documentation to deliver accurate and reliable insights.

# Datasources

- [FHIR Documentation](https://www.hl7.org/fhir/): Use official FHIR guides (e.g., Patient, Observation resources).

# Tech Stack

Frontend: Streamlit

Backend: LangChain 🦜🔗

Vectorstore: Pinecone 🌲

# Getting Started

## Prerequisites

- Python must be installed on local device. You can install it from
  the [Python installation guide](https://www.python.org/downloads/).
- uv must be installed, as it is used here as the dependency manager. You can install it from
  the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Environment Variables
| Variable                                      | Description                                                                                     |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------|
| `ENVIRONMENT`                                 | Application environment (Options: development, staging, production). Default: development.      |
| `APP_NAME`                                    | The name of the application. Default: MEDIUM_ANALYZER.                                          |
| `APP_VERSION`                                 | The version of the application. Default: 0.0.1.                                                |
| `PINECONE_API_KEY`                            | API key for Pinecone integration.                                                              |
| `PINECONE_INDEX_NAME`                         | Name of the Pinecone index. Default: fhir-resources-index.                                      |
| `AWS_ACCESS_KEY_ID`                           | AWS access key for integration.                                                                |
| `AWS_SECRET_ACCESS_KEY`                       | AWS secret access key for integration.                                                         |
| `AWS_REGION`                                  | AWS region for the service. Default: us-west-2.                                                |
| `EMBEDDING_MODEL_ID`                          | The ID for the embedding model. Default: amazon.titan-embed-text-v2:0.                         |
| `MODEL_ID`                                    | The model ID for the LLM. Default: us.anthropic.claude-3-7-sonnet-20250219-v1:0.               |
| `MODEL_TEMPERATURE`                           | Temperature setting for the LLM model (0.0 - 1.0). Default: 0.1.                               |
| `VECTOR_STORE_NUMBER_OF_DOCUMENTS_TO_RETRIEVE`| Number of documents to retrieve from the vector store. Default: 10.                            |
| `LANGSMITH_TRACING`                           | Enable or disable LangSmith tracing. Default: True.                                            |
| `LANGSMITH_ENDPOINT`                          | LangSmith API endpoint. Default: https://api.smith.langchain.com.                              |
| `LANGSMITH_API_KEY`                           | The API key for LangSmith integration.                                                         |
| `LANGSMITH_PROJECT`                           | The LangSmith project name. Default: default.                                                  |

## Setup

1. **Clone the repository**
    - cd into ice-breaker:
      ``` 
      cd fhir-resources-protocol-assistant
2. **Create `.env` File:**
    - Create a `.env` file inside the `./app` directory, where it contains source code.
3. **Setup virtual environment for the project**
    - Run in terminal:
      ``` 
      uv sync
      uv lock
    - After running commands this should create a .venv folder if not:
      ``` 
      uv venv
    - Choose the local python interpreter by selecting the current virtual environment in the used IDE.
    - Choose existing not generating new one, and select the following `.venv\Scripts\python.exe`.
4. **Run Project**
    - Run `uv run streamlit run frontend.py`.
