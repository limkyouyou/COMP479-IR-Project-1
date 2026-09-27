from collections import Counter
from collections.abc import Iterable

from nltk.corpus import stopwords


Document = tuple[int, list[str]]


def get_english_stop_words() -> set[str]:
    """Return the NLTK English stop-word vocabulary."""

    return set(stopwords.words("english"))


def rank_stop_words(
    documents: Iterable[Document],
) -> list[tuple[str, int]]:
    """
    Rank NLTK English stop words by frequency in the corpus.

    Terms with equal frequencies are ordered alphaetically to make the result deterministic.
    """

    stop_words = get_english_stop_words()
    frequencies: Counter[str] = Counter()

    for _, tokens in documents:
        for token in tokens:
            term = token.lower()

            if term in stop_words:
                frequencies[term] += 1

    return sorted(
        frequencies.items(), 
        key=lambda item: (-item[1], item[0]),
    )


def select_stop_words(
    ranked_stop_words: list[tuple[str, int]],
    count: int,
) -> set[str]:
    """Select the requested number of highest-frequency stop words."""

    return {term for term, _ in ranked_stop_words[:count]}