import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents import research_agent, writer_agent

class AgentState(TypedDict):
    topic: str             
    research_notes: str    
    final_article: str     

def call_researcher(state: AgentState) -> dict:
    topic = state["topic"]
    notes = research_agent(topic)
    return {"research_notes": notes}

def call_writer(state: AgentState) -> dict:
    topic = state["topic"]
    notes = state["research_notes"]
    article = writer_agent(topic, notes)
    return {"final_article": article}

workflow = StateGraph(AgentState)

workflow.add_node("researcher", call_researcher)
workflow.add_node("writer", call_writer)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

compiled_graph = workflow.compile()
