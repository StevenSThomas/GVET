"""Package used to interact with the Getty Vocabularies."""

from .api import Vocabulary

__all__ = [
    "vocabulary",
]

vocabulary = Vocabulary()
