from langgraph.constants import START, END
from langgraph.graph import StateGraph

from agents.nodes import (
    router_node,
    answer_node,
    comparison_node
)
from agents.state import AgentState


def build_graph(
        answer_service,
        comparison_service
):
    graph=StateGraph(AgentState)

    graph.add_node(
        "router",
        router_node
    )

    graph.add_node(
        "answer",
        lambda state: answer_node(state, answer_service)
    )

    graph.add_node(
        "comparison",
        lambda state:comparison_node(state, comparison_service)
    )

    graph.add_edge(START,"router")

    graph.add_conditional_edges(
        "router",

        lambda state: state["route"],

        {
            "ANSWER": "answer",
            "COMPARISON": "comparison"
        }
    )

    graph.add_edge(
        start_key="answer",
        end_key=END
    )

    graph.add_edge(
        start_key="comparison",
        end_key=END
    )

    return graph.compile()