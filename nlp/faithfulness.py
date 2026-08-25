import numpy as np

from nlp.embeddings import generate_embeddings
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


def cosine_similarity(
    vector_a: np.ndarray,
    vector_b: np.ndarray,
) -> float:
    """
    Calculate cosine similarity between two vectors.
    """

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b) / denominator
    )


def calculate_faithfulness(
    original_text: str,
    recall_text: str,
) -> dict:
    """
    Evaluate whether statements in the user's recall
    are supported by or contradict the original passage.

    For each recall sentence:

    1. Find the most semantically relevant sentence
       from the original passage.
    2. Use NLI to determine whether the recall sentence
       is entailed, neutral, or contradictory.
    """

    source_sentences = split_into_sentences(
        original_text
    )

    recall_sentences = split_into_sentences(
        recall_text
    )

    if not source_sentences or not recall_sentences:

        return {
            "faithfulness_score": 0.0,
            "entailments": [],
            "neutral_statements": [],
            "contradictions": [],
        }

    # ----------------------------------------------
    # Generate source sentence embeddings
    # ----------------------------------------------

    source_embeddings = generate_embeddings(
        source_sentences
    )

    # ----------------------------------------------
    # Generate recall sentence embeddings
    # ----------------------------------------------

    recall_embeddings = generate_embeddings(
        recall_sentences
    )

    entailments = []
    neutral_statements = []
    contradictions = []

    # ----------------------------------------------
    # Evaluate every recall sentence
    # ----------------------------------------------

    for index, recall_sentence in enumerate(
        recall_sentences
    ):

        recall_embedding = recall_embeddings[index]

        # Find the most semantically similar
        # source sentence.
        similarities = [
            cosine_similarity(
                recall_embedding,
                source_embedding,
            )
            for source_embedding in source_embeddings
        ]

        best_index = int(
            np.argmax(similarities)
        )

        best_source_sentence = (
            source_sentences[best_index]
        )

        best_similarity = similarities[best_index]

        # ------------------------------------------
        # NLI verification
        # ------------------------------------------

        result = classify_nli(
            premise=best_source_sentence,
            hypothesis=recall_sentence,
        )

        evaluation = {
            "statement": recall_sentence,
            "source_sentence": best_source_sentence,
            "similarity": round(
                best_similarity,
                4,
            ),
            "confidence": result["confidence"],
        }

        if result["label"] == "entailment":

            entailments.append(evaluation)

        elif result["label"] == "contradiction":

            contradictions.append(evaluation)

        else:

            neutral_statements.append(evaluation)

    # ----------------------------------------------
    # Calculate faithfulness score
    # ----------------------------------------------

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