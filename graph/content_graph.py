from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.content_agent import generate_challenge
from agents.content_validator_agent import (
    validate_challenge,
    is_valid,
)


# ==================================================
# STATE
# ==================================================

class ContentState(TypedDict, total=False):

    topic: str
    word_limit: int
    difficulty: str

    challenge: object
    validation_result: object

    attempts: int


# ==================================================
# CONTENT GENERATOR
# ==================================================

def content_generator_node(
    state: ContentState,
):
    """
    Generate a challenge using the content generation agent.
    """

    challenge = generate_challenge(
        topic=state["topic"],
        word_limit=state["word_limit"],
        difficulty=state["difficulty"],
    )

    attempts = state.get("attempts", 0) + 1

    return {
        "challenge": challenge,
        "attempts": attempts,
    }


# ==================================================
# CONTENT VALIDATOR
# ==================================================

def content_validator_node(
    state: ContentState,
):
    """
    Validate the generated challenge.
    """

    validation_result = validate_challenge(
        challenge=state["challenge"],
        word_limit=state["word_limit"],
    )

    return {
        "validation_result": validation_result,
    }


# ==================================================
# ROUTER
# ==================================================

def validation_router(
    state: ContentState,
):
    """
    Decide whether the generated challenge is valid.

    Valid:
        → END

    Invalid:
        → regenerate content
    """

    if is_valid(
        state["validation_result"]
    ):
        return "valid"

    return "invalid"


# ==================================================
# BUILD GRAPH
# ==================================================

def build_content_graph():

    graph = StateGraph(ContentState)

    # Nodes
    graph.add_node(
        "generate",
        content_generator_node,
    )

    graph.add_node(
        "validate",
        content_validator_node,
    )

    # START → Generator
    graph.add_edge(
        START,
        "generate",
    )

    # Generator → Validator
    graph.add_edge(
        "generate",
        "validate",
    )

    # Validator → Router
    graph.add_conditional_edges(
        "validate",
        validation_router,
        {
            "valid": END,
            "invalid": "generate",
        },
    )

    return graph.compile()


content_graph = build_content_graph()