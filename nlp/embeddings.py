from openai import embeddings

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model= SentenceTransformer(MODEL_NAME)

# Lets create a function to generate embeddings

def generate_embeddings(texts: list[str]):
    """
    I will generate embeddings for the given list of texts using the pretrained model"""
    return _model.encode(texts,
                         convert_to_tensor=True,
                         )