from openai import OpenAI

from agents.state import AgentState
from common.config import settings

client=OpenAI(api_key=settings.OPENAI_API_KEY)

def router_node(
        state:AgentState
):
    query=state["query"]
    response=client.responses.create(
        model="gpt-4.1-mini",
        instructions="""
        You are the routing component of SEC Sentinel.

Classify the user's question into exactly one category.

ANSWER:
The user wants information from a single filing.

COMPARISON:
The user wants to compare a current filing with a previous filing,
or asks what changed, was added, removed, or modified.

Return ONLY one of:

ANSWER
COMPARISON
""",
        input=query
    )

    route=response.output_text.strip().upper()
    if route not in ["ANSWER", "COMPARISON"]:
        route = "ANSWER"

    return{
        "route": route
    }

def answer_node(
        state:AgentState,
        answer_service
):
    result = answer_service.answer(
        ticker=state["ticker"],
        form_type=state["form_type"],
        filing_date=state["filing_date"],
        section=state["section"],
        query=state["query"]
    )

    return {
        "answer": result.text
    }

def comparison_node(
    state: AgentState,
    comparison_service
):

    result = comparison_service.compare(
        ticker=state["ticker"],
        form_type=state["form_type"],
        filing_date=state["filing_date"],
        section=state["section"],
        query=state["query"]
    )

    return {
        "answer": result.text
    }
