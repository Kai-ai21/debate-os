from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents import (
    proponent_agent,
    critic_agent,
    moderator_agent
)

# ═══════════════════════════════════════════════════
# STEP 1: DEFINE THE STATE
# ═══════════════════════════════════════════════════

class DebateState(TypedDict):
    decision: str
    context: str
    proponent_output: str
    critic_output: str
    moderator_output: dict


# ═══════════════════════════════════════════════════
# STEP 2: DEFINE THE NODE FUNCTIONS
# ═══════════════════════════════════════════════════

def proponent_node(state: DebateState) -> dict:
    """Node wrapper for the Proponent Agent."""

    print("[Graph] Proponent node running...")

    result = proponent_agent(
        state["decision"],
        state["context"]
    )

    return {
        "proponent_output": result
    }


def critic_node(state: DebateState) -> dict:
    """Node wrapper for the Critic Agent."""

    print("[Graph] Critic node running...")

    result = critic_agent(
        state["decision"],
        state["proponent_output"],
        state["context"]
    )

    return {
        "critic_output": result
    }


def moderator_node(state: DebateState) -> dict:
    """Node wrapper for the Moderator Agent."""

    print("[Graph] Moderator node running...")

    result = moderator_agent(
        state["decision"],
        state["proponent_output"],
        state["critic_output"],
        state["context"]
    )

    return {
        "moderator_output": result
    }


# ═══════════════════════════════════════════════════
# STEP 3: BUILD AND COMPILE THE GRAPH
# ═══════════════════════════════════════════════════

def build_debate_graph():
    """Build and return the compiled debate graph."""

    graph = StateGraph(DebateState)

    graph.add_node("proponent", proponent_node)
    graph.add_node("critic", critic_node)
    graph.add_node("moderator", moderator_node)

    graph.set_entry_point("proponent")

    graph.add_edge("proponent", "critic")
    graph.add_edge("critic", "moderator")
    graph.add_edge("moderator", END)

    return graph.compile()


# ═══════════════════════════════════════════════════
# STEP 4: TEST THE GRAPH
# ═══════════════════════════════════════════════════

if __name__ == "__main__":

    debate_graph = build_debate_graph()

    initial_state = {
        "decision": "Should I quit college to start a startup?",
        "context": "2 co-founders, product idea, 6 months savings",
        "proponent_output": "",
        "critic_output": "",
        "moderator_output": {}
    }

    print("Starting debate graph...\n")

    result = debate_graph.invoke(initial_state)

    print("\n✅ Graph complete. Final state keys:\n")

    for key, value in result.items():
        preview = (
            str(value)[:80] + "..."
            if len(str(value)) > 80
            else str(value)
        )

        print(f"{key}: {preview}")