from langchain_core.messages import SystemMessage

from llm import model
from state import State


def chatbot(state: State):
    sys_msg = SystemMessage(content="You are a helpful assistant.")

    return {"messages": [model.invoke([sys_msg] + state["messages"])]}
