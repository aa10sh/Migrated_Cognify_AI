from pydantic import BaseModel, Field

from models.llm import client, MODEL_NAME


class FinalEvaluationResult(BaseModel):
    final_score: float = Field(
        ge=0,
        le=100,
    )

    performance_level: str

    strengths: list[str]

    missed_areas: list[str]

    feedback: str


def evaluate_final_result(
    semantic_result: dict,
    concept_coverage_result: dict,
    faithfulness_result: dict,
    language_coherence_result: dict,
) -> FinalEvaluationResult:
    """
    Combine the outputs of the independent evaluation agents
    and generate the final Cognify evaluation.

    The Final Evaluator does not perform the underlying NLP
    evaluation itself. It interprets the results produced by
    the independent evaluators.
    """
    # Edge case: user left the typing space blank or submitted no text
    if (
        float(semantic_result.get("score", 0)) == 0.0
        and float(concept_coverage_result.get("score", 0)) == 0.0
        and float(language_coherence_result.get("overall_score", 0)) == 0.0
    ):
        missed = concept_coverage_result.get("missed_concepts") or [
            "All concepts from the passage were missed because no response was provided."
        ]
        return FinalEvaluationResult(
            final_score=0.0,
            performance_level="Poor",
            strengths=[],
            missed_areas=missed,
            feedback="You did not type anything. No recall response was captured to evaluate. Please write what you remember from the passage to receive an evaluation score.",
        )

    prompt = f"""
You are the Final Evaluation Agent for Cognify AI.

Your job is to combine the results produced by four
independent evaluation agents and generate the final
assessment of the user's recall.

The four evaluators are:

1. Semantic Evaluation
   Measures overall semantic similarity between the
   original passage and the user's recall.

2. Concept Coverage Evaluation
   Measures how many important concepts from the
   original passage were remembered.

3. Faithfulness Evaluation
   Measures whether claims made in the user's recall
   are supported by the original passage and identifies
   contradictions.

4. Language and Coherence Evaluation
   Measures grammar, clarity, coherence, and organization
   of the user's response.

IMPORTANT RULES:

- Do not perform a new semantic analysis.
- Do not invent scores.
- Do not change the evaluator scores.
- Use the provided evaluator outputs as evidence.
- Do not reward the user twice for the same characteristic.
- Do not penalize the user for missing concepts under
  the language evaluation.
- Do not treat neutral statements as contradictions.
- Contradictions should negatively affect the final assessment.
- Keep the final feedback understandable to a normal user.
- Do not expose internal agent architecture, model names,
  or implementation details.

FINAL SCORE WEIGHTING:

Use the following weighting:

Semantic Similarity: 25%
Concept Coverage:    35%
Faithfulness:        25%
Language/Coherence:  15%

Convert all component scores to a 0-100 scale before
applying the weights.

The final score must remain between 0 and 100.

PERFORMANCE LEVEL:

90-100 → Excellent
75-89  → Strong
60-74  → Moderate
40-59  → Weak
0-39   → Poor

Generate:

1. final_score
2. performance_level
3. strengths
4. missed_areas
5. concise and constructive feedback

The feedback should explain:
- what the user remembered well
- what important areas were missed
- whether the recall contained inaccurate/contradictory claims
- one or two useful suggestions for improving recall

Do not simply repeat the raw evaluator outputs.

---------------------------------------
SEMANTIC EVALUATION
---------------------------------------

{semantic_result}

---------------------------------------
CONCEPT COVERAGE EVALUATION
---------------------------------------

{concept_coverage_result}

---------------------------------------
FAITHFULNESS EVALUATION
---------------------------------------

{faithfulness_result}

---------------------------------------
LANGUAGE & COHERENCE EVALUATION
---------------------------------------

{language_coherence_result}

---------------------------------------

Return the final evaluation using the required schema.
"""

    response = client.responses.parse(
        model=MODEL_NAME,
        input=prompt,
        text_format=FinalEvaluationResult,
    )

    return response.output_parsed