from langgraph.graph.state import StateGraph, CompiledStateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from ai.state import State
from ai.attendance_agent import attendance_agent

def create_graph() -> CompiledStateGraph:
    checkpointer = MemorySaver()

    graph = StateGraph(State)

    graph.add_node("attendance_agent", attendance_agent)


    graph.add_edge(START, "attendance_agent")
    graph.add_edge("attendance_agent", "attendance_agent_2")
    graph.add_edge("attendance_agent_2", END)

    return graph.compile(checkpointer=checkpointer)