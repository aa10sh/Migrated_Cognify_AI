from models.challenge import Challenge
from models.llm import client, MODEL_NAME
from agents.content_validator_agent import (
    validate_challenge,
    is_valid,
)


MAX_GENERATION_ATTEMPTS = 3


def generate_challenge(
    topic: str,
    word_limit: int,
    difficulty: str,
) -> Challenge:

    previous_issues = []
    last_challenge = None

    for attempt in range(1, MAX_GENERATION_ATTEMPTS + 1):

        feedback_section = ""
        if previous_issues:
            feedback_section = f"\nNote: The previous attempt had the following issues to correct: {', '.join(previous_issues)}. Please ensure the content is tailored appropriately."

        prompt = f"""
You are the Content Generation Agent for Cognify AI.

Generate a reading passage for a memory and recall challenge.

Topic: {topic}
Target word limit: {word_limit} words
Difficulty: {difficulty}
{feedback_section}

Requirements:

1. The passage must be relevant to the requested topic.
2. The passage should be coherent and informative.
3. The passage should match the requested difficulty.
4. Keep the passage within a reasonable range of the requested word limit.
5. Include multiple meaningful facts or ideas that can later be evaluated.
6. Identify the important concepts from the passage.
7. Do not include the key concepts as a separate section inside the passage.
8. The key concepts should represent information that a user should ideally remember.
9. Never merge two or more words to manipulate the word count.
10. Preserve normal spaces between all words.
11. Do not remove spaces, punctuation spacing, or otherwise alter whitespace
    to reach the target word count.
12. The word limit is a target. Prioritize natural, readable and coherent
    content over reaching an exact number.
13. Do not artificially manipulate the text to satisfy the word limit.

Return the result using the required Challenge structure.
"""

        response = client.responses.parse(
            model=MODEL_NAME,
            input=prompt,
            text_format=Challenge,
        )

        challenge = response.output_parsed
        last_challenge = challenge

        validation = validate_challenge(
            challenge,
            word_limit,
        )

        if is_valid(validation):
            # Store the actual Python-calculated word count.
            challenge.word_count = len(challenge.content.split())

            return challenge

        print(
            f"Challenge validation failed "
            f"(attempt {attempt}/{MAX_GENERATION_ATTEMPTS})"
        )
        print("Issues:", validation.issues)
        previous_issues = validation.issues

    # Graceful degradation on final attempt if topic-relevant and coherent
    if last_challenge and getattr(validation, 'topic_relevant', True) and getattr(validation, 'coherent', True):
        last_challenge.word_count = len(last_challenge.content.split())
        return last_challenge

    raise ValueError(
        "Unable to generate a valid challenge after "
        f"{MAX_GENERATION_ATTEMPTS} attempts."
    )