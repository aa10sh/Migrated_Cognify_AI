from torch.nn.functional import cosine_similarity
from nlp.embeddings import generate_embeddings

def calculate_semantic_similarity(
    original_text: str,
    recall_text: str,
) -> float:
    """
    Calculate semantic similarity between the original passage
    and the user's recall.

    Returns a score between 0 and 1.
    """

    embeddings = generate_embeddings(
        [original_text, recall_text]
    )

    original_embedding = embeddings[0].unsqueeze(0)
    recall_embedding = embeddings[1].unsqueeze(0)

    similarity = cosine_similarity(
        original_embedding,
        recall_embedding,
    )

    return float(similarity.item())