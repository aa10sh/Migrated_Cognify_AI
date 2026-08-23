from nlp.embeddings import generate_embeddings
from torch.nn.functional import cosine_similarity


DEFAULT_COVERAGE_THRESHOLD = 0.55


def calculate_concept_coverage(
    key_concepts: list[str],
    recall_text: str,
    threshold: float = DEFAULT_COVERAGE_THRESHOLD,
) -> dict:
    """
    Determine how many important concepts from the original passage
    are represented in the user's recall.
    """

    if not key_concepts:
        return {
            "coverage_score": 0.0,
            "covered_concepts": [],
            "missed_concepts": [],
            "concept_scores": [],
        }

    if not recall_text.strip():
        return {
            "coverage_score": 0.0,
            "covered_concepts": [],
            "missed_concepts": key_concepts,
            "concept_scores": [],
        }

    texts = key_concepts + [recall_text]

    embeddings = generate_embeddings(texts)

    concept_embeddings = embeddings[:-1]
    recall_embedding = embeddings[-1].unsqueeze(0)

    covered_concepts = []
    missed_concepts = []
    concept_scores = []

    for concept, concept_embedding in zip(
        key_concepts,
        concept_embeddings,
    ):
        similarity = cosine_similarity(
            concept_embedding.unsqueeze(0),
            recall_embedding,
        ).item()

        concept_scores.append(
            {
                "concept": concept,
                "similarity": round(similarity, 4),
            }
        )

        if similarity >= threshold:
            covered_concepts.append(concept)
        else:
            missed_concepts.append(concept)

    coverage_score = (
        len(covered_concepts) / len(key_concepts)
    )

    return {
        "coverage_score": round(coverage_score, 4),
        "covered_concepts": covered_concepts,
        "missed_concepts": missed_concepts,
        "concept_scores": concept_scores,
    }