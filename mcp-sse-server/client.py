# Create server parameters for stdio connection
import asyncio

from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatBedrockConverse(
    model='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
    temperature=0.1,
)


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    max_iterations = 3
    recursion_limit = 2 * max_iterations + 1
    tools = await client.get_tools()
    agent_name = "MathAgent"
    system_message = "You are a precise and efficient assistant for performing mathematical operations."

    agent = create_react_agent(name=agent_name, model=llm, prompt=system_message, tools=tools)
    result = await agent.ainvoke({"messages": "What is 2 + 2?"},
                                 {"recursion_limit": recursion_limit}, debug=True)

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
