import sys
import os

from dotenv import load_dotenv, find_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings


def get_embedding(embedding_model_name: str):
    """
    Get embedding model.

    Supported embedding models:

    OPENAI:
        - text-embedding-ada-002
    """
    _ = load_dotenv(find_dotenv())
    embedding = OpenAIEmbeddings()

    return embedding
