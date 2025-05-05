from typing import Union, List

from langchain.agents.format_scratchpad import format_log_to_str
from langchain.schema import AgentAction, AgentFinish
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool, tool
from loguru import logger

from clients.llm_client import LLMClient
from config.logger import setup_logging
from config.settings import get_settings

setup_logging()
settings = get_settings()
llm_client = LLMClient()


@tool("get_text_length")
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non-alphabetic characters just in case

    return len(text)


def clean_tool_name(tool_name: str) -> str:
    """
    Cleans up the tool name by removing extra spaces and symbols.

    Args:
        tool_name (str): The raw tool name.

    Returns:
        str: The cleaned tool name.
    """
    # Remove extra spaces, newlines, and symbols
    cleaned_name = tool_name.strip().strip('#').strip()
    return cleaned_name


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


if __name__ == '__main__':
    logger.info("Hello ReAct LangChain!")

    tools = [get_text_length]

    template = """
    You are a ReAct (Reasoning and Acting) agent tasked with goal is to reason about the query and decide on the best course of action to answer it accurately.
    
    Available tools: {tools}
    
    Remember:
    - Be thorough in your reasoning.
    - Use tools when you need more information.
    - Always base your reasoning on the actual observations from tool use.
    - If a tool returns no results or fails, acknowledge this and consider using a different tool or approach.
    - Provide a final answer only when you're confident you have sufficient information.
    - If you cannot find the necessary information after using available tools, admit that you don't have enough information to answer the query confidently.
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    intermediate_steps = []
    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        logger.info(f"Agent Step: {agent_step}")
        template_variables = {
            "input": "What is the length of the word: OMAR",
            "agent_scratchpad": format_log_to_str(intermediate_steps)
        }

        agent_step: Union[AgentAction, AgentFinish] = llm_client.generate_response(prompt, template_variables)
        logger.debug(agent_step.type)

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            logger.info(f"{observation=}")
            intermediate_steps.append((agent_step, str(observation)))

    if isinstance(agent_step, AgentFinish):
        logger.info(agent_step.return_values)
