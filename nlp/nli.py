from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/nli-MiniLM2-L6-H768"

_model = CrossEncoder(MODEL_NAME)


def classify_nli(
    premise: str,
    hypothesis: str,
) -> dict:
    """
    Classify the relationship between a premise and hypothesis.

    Returns:
        label:
            entailment, contradiction, or neutral

        confidence:
            probability of the predicted label
    """

    scores = _model.predict(
        [(premise, hypothesis)],
        apply_softmax=True,
    )

    predicted_index = scores[0].argmax()

    labels = [
        "contradiction",
        "entailment",
        "neutral",
    ]

    return {
        "label": labels[predicted_index],
        "confidence": round(
            float(scores[0][predicted_index]),
            4,
        ),
    }