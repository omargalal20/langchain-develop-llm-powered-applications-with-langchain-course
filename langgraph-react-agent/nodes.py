from llm import model
from state import State


def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}
