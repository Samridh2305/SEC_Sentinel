from openai import OpenAI, OpenAIError

from agents.state import AgentState
from common.config import settings
from common.logger import logger
from exceptions.custom_exceptions import ServiceException
from schema.schema import RouteDecision

client=OpenAI(api_key=settings.OPENAI_API_KEY)

def router_node(
        state:AgentState
):
    # Supplying an exact comparison date is an explicit comparison request.
    if state.get("comparison_filing_date"):
        return {"route": "COMPARISON"}

    query=state["query"]
    try:
        response=client.responses.parse(
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
            input=query,
            text_format=RouteDecision
        )
    except OpenAIError as exc:
        logger.exception("Could not route user question")
        raise ServiceException("The AI service is temporarily unavailable.") from exc

    route = response.output_parsed.route

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
        comparison_filing_date=state["comparison_filing_date"],
        section=state["section"],
        query=state["query"]
    )

    return {
        "answer": result.text
    }
