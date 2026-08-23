from pydantic import BaseModel, Field

from nlp.faithfulness import calculate_faithfulness


class FaithfulnessEvaluationResult(BaseModel):
    faithfulness_score: float = Field(
        ge=0,
        le=1,
    )

    score: float = Field(
        ge=0,
        le=100,
    )

    entailments: list[dict]

    neutral_statements: list[dict]

    contradictions: list[dict]


def evaluate_faithfulness(
    original_text: str,
    recall_text: str,
) -> FaithfulnessEvaluationResult:
    """
    Evaluate whether the user's recalled statements are
    supported by or contradict the original passage.
    """

    result = calculate_faithfulness(
        original_text=original_text,
        recall_text=recall_text,
    )

    faithfulness_score = result[
        "faithfulness_score"
    ]

    return FaithfulnessEvaluationResult(
        faithfulness_score=faithfulness_score,
        score=round(
            faithfulness_score * 100,
            2,
        ),
        entailments=result["entailments"],
        neutral_statements=result["neutral_statements"],
        contradictions=result["contradictions"],
    )