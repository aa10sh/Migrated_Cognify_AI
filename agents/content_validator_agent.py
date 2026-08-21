from pydantic import BaseModel, Field

from models.challenge import Challenge
from models.llm import client, MODEL_NAME


class ValidationResult(BaseModel):
    word_count_valid: bool = Field(
        description="Whether the actual content word count is within the requested limit."
    )

    topic_relevant: bool = Field(
        description="Whether the passage is relevant to the requested topic."
    )

    coherent: bool = Field(
        description="Whether the passage is logically organized and coherent."
    )

    difficulty_appropriate: bool = Field(
        description="Whether the passage matches the requested difficulty."
    )

    sufficient_information: bool = Field(
        description="Whether the passage contains enough meaningful information for later recall evaluation."
    )

    issues: list[str] = Field(
        description="Specific problems found in the generated challenge."
    )


def count_words(text: str) -> int:
    """Calculate the actual number of words in the generated content."""
    return len(text.split())


def validate_challenge(
    challenge: Challenge,
    target_word_count: int,
) -> ValidationResult:

    actual_word_count = count_words(challenge.content)

    # Allow a 10% tolerance around the requested word count.
    minimum_words = int(target_word_count * 0.90)
    maximum_words = int(target_word_count * 1.10)

    word_count_valid = (
        minimum_words <= actual_word_count <= maximum_words
    )

    prompt = f"""
You are the Content Validation Agent for Cognify AI.

Your job is to verify whether a generated reading challenge is suitable
for the user.

Original challenge requirements:

Topic:
{challenge.topic}

Requested word count:
{target_word_count}

Requested difficulty:
{challenge.difficulty}

Generated content:
{challenge.content}

Generated key concepts:
{challenge.key_concepts}

Evaluate ONLY these qualitative criteria:

1. Topic relevance
   - Is the passage meaningfully related to the requested topic?

2. Coherence
   - Is the passage logically organized?
   - Do the ideas connect naturally?

3. Difficulty
   - Does the passage appropriately match the requested difficulty?

4. Sufficient useful information
   - Does the passage contain enough meaningful facts, ideas, or concepts
     to support a later memory and recall evaluation?

Return specific issues when a criterion fails.

Do not evaluate the word count yourself.
The actual word count is calculated programmatically.
"""

    response = client.responses.parse(
        model=MODEL_NAME,
        input=prompt,
        text_format=ValidationResult,
    )

    result = response.output_parsed

    # The word-count result must come from deterministic Python logic.
    result.word_count_valid = word_count_valid

    # Add a deterministic word-count issue when necessary.
    if not word_count_valid:
        result.issues.append(
            f"Actual word count is {actual_word_count}; "
            f"expected approximately {target_word_count} words."
        )

    return result


def is_valid(result: ValidationResult) -> bool:
    """
    Determine whether the generated challenge passes all
    required validation criteria.
    """

    return (
        result.word_count_valid
        and result.topic_relevant
        and result.coherent
        and result.difficulty_appropriate
        and result.sufficient_information
    )