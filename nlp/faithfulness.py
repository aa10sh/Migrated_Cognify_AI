from nlp.nli import classify_nli


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into simple sentences.
    """

    normalized_text = (
        text
        .replace("!", ".")
        .replace("?", ".")
    )

    sentences = [
        sentence.strip()
        for sentence in normalized_text.split(".")
        if sentence.strip()
    ]

    return sentences


def calculate_faithfulness(
    original_text: str,
    recall_text: str,
) -> dict:
    """
    Evaluate whether statements in the user's recall
    are supported by or contradict the original passage.
    """

    recall_sentences = split_into_sentences(
        recall_text
    )

    if not recall_sentences:

        return {
            "faithfulness_score": 0.0,
            "entailments": [],
            "neutral_statements": [],
            "contradictions": [],
        }

    entailments = []
    neutral_statements = []
    contradictions = []

    for sentence in recall_sentences:

        result = classify_nli(
            premise=original_text,
            hypothesis=sentence,
        )

        if result["label"] == "entailment":

            entailments.append({
                "statement": sentence,
                "confidence": result["confidence"],
            })

        elif result["label"] == "contradiction":

            contradictions.append({
                "statement": sentence,
                "confidence": result["confidence"],
            })

        else:

            neutral_statements.append({
                "statement": sentence,
                "confidence": result["confidence"],
            })

    total = len(recall_sentences)

    entailment_count = len(entailments)
    contradiction_count = len(contradictions)

    faithfulness_score = (
        entailment_count
        - (0.5 * contradiction_count)
    ) / total

    faithfulness_score = max(
        0.0,
        min(
            1.0,
            faithfulness_score,
        ),
    )

    return {
        "faithfulness_score": round(
            faithfulness_score,
            4,
        ),
        "entailments": entailments,
        "neutral_statements": neutral_statements,
        "contradictions": contradictions,
    }