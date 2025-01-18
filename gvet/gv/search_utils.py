"""utility functions for cleaning a search term to pass to lucene"""

import string

STOP_WORDS = [
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "if",
    "in",
    "into",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "such",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "was",
    "will",
    "with",
]


def clean_search_terms(text: str) -> str:
    cleaned_text = replace_punctuation_with_space(text)
    words = cleaned_text.split(" ")
    words = remove_stop_words(words)
    words = add_wildcard(words)
    words = add_conjunction(words)
    return " ".join(words)


def replace_punctuation_with_space(text: str) -> str:
    return "".join(
        [" " if char in string.punctuation else char for char in text]
    ).strip()


def remove_stop_words(words: list[str]) -> list[str]:
    """remove STOP words from the search text"""
    return [word for word in words if word not in STOP_WORDS]


def add_wildcard(words: list[str]) -> list[str]:
    """adds a wildcard after each word"""
    return [w + "*" for w in words]


def add_conjunction(words: list[str]) -> list[str]:
    """add AMD betweem each word"""
    modified_words = [f"{w} AND" for w in words]
    # remove the last AND
    modified_words[-1] = modified_words[-1][:-4]
    return modified_words
