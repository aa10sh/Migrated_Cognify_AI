from pydantic import BaseModel, Field

from models.llm import client, MODEL_NAME


class LanguageCoherenceResult(BaseModel):
    grammar_score: float = Field(
        ge=0,
        le=100,
    )

    clarity_score: float = Field(
        ge=0,
        le=100,
    )

    coherence_score: float = Field(
        ge=0,
        le=100,
    )

    organization_score: float = Field(
        ge=0,
        le=100,
    )

    overall_score: float = Field(
        ge=0,
        le=100,
    )

    strengths: list[str]

    issues: list[str]

    feedback: str


def evaluate_language_coherence(
    recall_text: str,
) -> LanguageCoherenceResult:
    """
    Evaluate the linguistic quality and coherence of the
    user's recalled response.

    This evaluator focuses only on the user's writing quality.
    It does not evaluate factual correctness or concept coverage.
    """

    if not recall_text.strip():
        return LanguageCoherenceResult(
            grammar_score=0,
            clarity_score=0,
            coherence_score=0,
            organization_score=0,
            overall_score=0,
            strengths=[],
            issues=["No recall response was provided."],
            feedback=(
                "No response was provided, so language and "
                "coherence could not be evaluated."
            ),
        )

    prompt = f"""
You are the Language and Coherence Evaluation Agent
for Cognify AI.

Your responsibility is ONLY to evaluate the linguistic
quality of the user's recall response.

Do NOT evaluate:
- Whether the information is factually correct.
- Whether important concepts were remembered.
- Semantic similarity to the original passage.
- Whether the response contains information from the source.

Those aspects are handled by other independent evaluators.

Evaluate the response using these dimensions:

1. Grammar
   - Sentence construction
   - Grammar errors
   - Word usage
   - Basic punctuation

2. Clarity
   - Whether ideas are understandable
   - Whether sentences communicate ideas clearly
   - Avoid unnecessary ambiguity

3. Coherence
   - Whether ideas connect logically
   - Whether the response flows naturally
   - Whether there are abrupt or confusing transitions

4. Organization
   - Logical ordering of ideas
   - Paragraph structure
   - Overall readability

Scoring:
- 90-100: Excellent
- 75-89: Good
- 60-74: Fair
- 40-59: Weak
- 0-39: Poor

Important:
- Evaluate the writing that is actually present.
- Do not penalize the user for missing information from
  the original passage.
- Do not reward the response for factual correctness.
- Do not invent problems that are not present.
- Keep feedback concise and useful.

Return JSON matching the required schema.

USER RECALL:

{recall_text}
"""

    response = client.responses.parse(
        model=MODEL_NAME,
        input=prompt,
        text_format=LanguageCoherenceResult,
    )

    return response.output_parsed