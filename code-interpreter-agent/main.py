from dotenv import load_dotenv

from code_interpreter_agent import CodeInterpreterAgent
from langsmith_client import LangSmithClient
from llm_client import LLMClient
from logger import setup_logging

if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    llm_client = LLMClient()
    langsmith_client = LangSmithClient()
    code_interpreter_agent = CodeInterpreterAgent(llm_client, langsmith_client)

    first_query = "Which season has the most episodes?"
    code_interpreter_agent.interpret(first_query)

    second_query = "Generate and save in current working directory 15 qrcodes that point to `www.udemy.com/course/langchain`"
    code_interpreter_agent.interpret(second_query)
