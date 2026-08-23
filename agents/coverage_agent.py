from pydantic import BaseModel, Field

from nlp.coverage import calculate_concept_coverage


class ConceptEvaluationResult(BaseModel):
    coverage_score: float = Field(
        ge=0,
        le=1,
    )

    score: float = Field(
        ge=0,
        le=100,
    )

    covered_concepts: list[str]

    missed_concepts: list[str]

    concept_scores: list[dict]


def evaluate_concept_coverage(
    key_concepts: list[str],
    recall_text: str,
) -> ConceptEvaluationResult:
    """
    Evaluate how many important concepts from the original
    challenge were represented in the user's recall.
    """

    result = calculate_concept_coverage(
        key_concepts=key_concepts,
        recall_text=recall_text,
    )

    coverage_score = result["coverage_score"]

    return ConceptEvaluationResult(
        coverage_score=coverage_score,
        score=round(
            coverage_score * 100,
            2,
        ),
        covered_concepts=result["covered_concepts"],
        missed_concepts=result["missed_concepts"],
        concept_scores=result["concept_scores"],
    )