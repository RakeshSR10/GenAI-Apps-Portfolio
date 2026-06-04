import warnings
# Suppress structural warning alerts right from line 1
warnings.filterwarnings("ignore", category=DeprecationWarning)

from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents import research_agent, writer_agent, critic_agent

# 1. Define the Shared Memory Schema Tracker
class FactoryState(TypedDict):
    topic: str             # Target theme query
    research_notes: str    # Output notes from researcher
    article_draft: str     # Output report draft from writer
    critic_feedback: str   # Review comments from critic
    loop_count: int        # Counter to prevent infinite loops

# 2. Define Node Functions
def researcher_node(state: FactoryState) -> dict:
    """Node 1: Pulls facts from the live internet."""
    notes = research_agent(state["topic"])
    return {"research_notes": notes, "loop_count": 0}

def writer_node(state: FactoryState) -> dict:
    """Node 2: Compiles or rewrites the text report draft."""
    current_loops = state.get("loop_count", 0) + 1
    draft = writer_agent(
        topic=state["topic"],
        research_notes=state["research_notes"],
        critic_feedback=state["critic_feedback"]
    )
    return {"article_draft": draft, "loop_count": current_loops}

def critic_node(state: FactoryState) -> dict:
    """Node 3: Audits quality and sets feedback metrics."""
    feedback = critic_agent(state["topic"], state["article_draft"])
    return {"critic_feedback": feedback}

# 3. Define the Router: Conditional Routing Logic Evaluation function
def route_approval_condition(state: FactoryState) -> str:
    """
    Evaluates the state parameters to determine if the workflow 
    should stop or route back for a rewrite.
    """
    feedback_text = state["critic_feedback"].strip()
    
    # Safety Check: Stop loops if the agents have rewritten the draft 3 times
    if state.get("loop_count", 0) >= 3:
        return "stop_workflow"
        
    # Check if the auditor agent outputted the exact approval token
    if feedback_text == "APPROVE":
        return "stop_workflow"
    else:
        # Route back to writer node for a correction loop
        return "loop_to_writer"

# 4. Construct the Graph Workflow Workflow Layout
builder = StateGraph(FactoryState)

# Add Processing Units as Graph Nodes
builder.add_node("researcher_agent", researcher_node)
builder.add_node("writer_agent", writer_node)
builder.add_node("critic_agent", critic_node)

# Connect Nodes with Structural Edges
builder.set_entry_point("researcher_agent")
builder.add_edge("researcher_agent", "writer_agent")
builder.add_edge("writer_agent", "critic_agent")

# Add the Conditional Router Routing path to check the Critic's decision
builder.add_conditional_edges(
    "critic_agent",
    route_approval_condition,
    {
        "stop_workflow": END,
        "loop_to_writer": "writer_agent"
    }
)

# Compile into an active structural executable engine instance
compiled_factory_graph = builder.compile()