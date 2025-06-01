from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langsmith import Client
from loguru import logger

from llm import tools
from nodes import chatbot
from state import State

load_dotenv()

if __name__ == "__main__":
    logger.info("ReActAgent using LangGraph")

    max_iterations = 3
    recursion_limit = 2 * max_iterations + 1
    client = Client()

    graph_builder = StateGraph(State)

    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    graph = graph_builder.compile()

    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

    query_prompt = "What is the weather in SF? List it and then Triple it."
    response = graph.invoke({"messages": [{"role": "user", "content": query_prompt}]},
                            {"recursion_limit": recursion_limit}, debug=True)
    logger.info(response["messages"][-1].content)
