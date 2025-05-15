from typing import Any

from dotenv import load_dotenv
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.utilities import PythonREPL
from loguru import logger

from langsmith_client import LangSmithClient
from llm_client import LLMClient

load_dotenv()


class CodeInterpreterAgent:
    """
    CodeInterpreterAgent
    """

    def __init__(
            self,
            llm_client: LLMClient,
            langsmith_client: LangSmithClient,
    ):
        """
        Initialize CodeInterpreterAgent configuration.
        """
        self.agent_name = "CodeInterpreterAgent"
        self.llm = llm_client.get_llm()
        self.react_prompt = langsmith_client.get_prompt("langchain-ai/react-agent-template")

        # Create Python REPL tool
        python_repl = PythonREPL()
        self.repl_tool = Tool(
            name="python_repl",
            description="A Python shell. Use this to execute Python commands. Input should be a valid Python command. If you want to see the output of a value, you should print it out with `print(...)`.",
            func=python_repl.run,
        )

    def interpret(self, query_text: str):
        """
        Use the agent to interpret codes.
        """
        logger.info(f"{self.agent_name} processing query: {query_text}")

        instructions_template = """
            # Personality
            You are a thoughtful and analytical assistant who excels at interpreting code, performing calculations, and solving computational problems efficiently.

            # Guardrails
            - Always validate input before execution.
            - If you get an error, debug your code and try again.
            - Always validate the code and output even if you know the answer without executing the code.
            - Avoid executing potentially harmful commands like deleting files or accessing restricted resources.
            - Respond with clear, concise outputs, providing explanations only when requested.
            - If execution contains executing potentially harmful commands like deleting files or accessing restricted resources, refuse
            to execute and terminate the execution immediately.
            - If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.

            # Tools
            You have access to a Python REPL tool. Use it to:
            - Execute Python code.
            - Perform calculations or test logic.
            - Simulate simple scenarios for better understanding.
            
            Query: {query_text}
        """

        prompt_template = PromptTemplate(
            input_variables=["query_text"],
            template=instructions_template,
        )

        tools_for_agent = [self.repl_tool]
        python_agent = create_react_agent(
            prompt=prompt_template,
            llm=self.llm,
            tools=tools_for_agent,
        )

        python_agent_executor = AgentExecutor(agent=python_agent, tools=tools_for_agent, verbose=True)

        csv_agent_executor: AgentExecutor = create_csv_agent(
            llm=self.llm,
            path="episode_info.csv",
            verbose=True,
        )

        def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
            return python_agent_executor.invoke({"input": original_prompt})

        tools = [
            Tool(
                name="Python Agent",
                func=python_agent_executor_wrapper,
                description="""useful when you need to transform natural language to python and execute the python code,
                              returning the results of the code execution
                              DOES NOT ACCEPT CODE AS INPUT""",
            ),
            Tool(
                name="CSV Agent",
                func=csv_agent_executor.invoke,
                description="""useful when you need to answer question over episode_info.csv file,
                             takes an input the entire question and returns the answer after running pandas calculations""",
            ),
        ]
        grand_agent = create_react_agent(
            prompt=prompt_template,
            llm=self.llm,
            tools=tools,
        )
        grand_agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True)

        print(
            grand_agent_executor.invoke(
                {
                    "input": query_text,
                }
            )
        )
