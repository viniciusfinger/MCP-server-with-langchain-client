from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict

class State(TypedDict):
    thread_id: str
    messages: Annotated[list[AnyMessage], add_messages]