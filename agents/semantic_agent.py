from pydantic import BaseModel, Field

from nlp.similarity import calculate_semantic_similarity


class SemanticEvaluationResult(BaseModel):
    semantic_similarity: float = Field(
        ge=0,
        le=1,
    )

    score: float = Field(
        ge=0,
        le=100,
    )

    interpretation: str


def evaluate_semantic_similarity(
    original_text: str,
    recall_text: str,
) -> SemanticEvaluationResult:
    """
    Evaluate the overall semantic similarity between
    the original passage and the user's recall.
    """

    if not recall_text.strip():

        return SemanticEvaluationResult(
            semantic_similarity=0.0,
            score=0.0,
            interpretation="No recall response was provided.",
        )

    similarity = calculate_semantic_similarity(
        original_text,
        recall_text,
    )

    score = similarity * 100

    if score >= 85:
        interpretation = "Very high semantic similarity."

    elif score >= 70:
        interpretation = "Strong semantic similarity."

    elif score >= 50:
        interpretation = "Moderate semantic similarity."

    elif score >= 30:
        interpretation = "Low semantic similarity."

    else:
        interpretation = "Very low semantic similarity."

    return SemanticEvaluationResult(
        semantic_similarity=round(similarity, 4),
        score=round(score, 2),
        interpretation=interpretation,
    )