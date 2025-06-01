from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

load_dotenv()


@tool("triple")
def triple(num: float) -> float:
    """
    Receives a number and triples it

    :param num: a number to triple
    :return: the number tripled ->  multiplied by 3
    """
    return 3 * float(num)

tools = [TavilySearch(max_results=1), triple]

model = ChatBedrockConverse(
    model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
    temperature=0.1,
)

model = model.bind_tools(tools)


