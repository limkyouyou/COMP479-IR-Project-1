from collections import Counter
from collections.abc import Iterable

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


Document = tuple[int, list[str]]


_stemmer = PorterStemmer()


def remove_punctuation(
    tokens: list[str],
) -> list[str]:
    """Remove tokens that contain no alphanumeric characters."""

    return [token for token in tokens if any(char.isalnum() for char in token)]


def remove_numbers(
    tokens: list[str],
) -> list[str]:
    """Remove tokens consisting entirely of digits."""

    return [token for token in tokens if not token.isdigit()]


def case_fold(
    tokens: list[str],
) -> list[str]:
    """Convert all tokens to lowercase."""

    return [token.lower() for token in tokens]


def remove_stop_words(
    tokens: list[str],
    stop_words: set[str],
) -> list[str]:
    """Remove tokens contained in the supplied stop-word set."""

    return [token for token in tokens if token not in stop_words]


def stem_tokens(
    tokens: list[str],
) -> list[str]:
    """Apply Porter stemming to all tokens."""

    return [_stemmer.stem(token) for token in tokens]


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


def compute_index_statistics(
    documents: Iterable[Document],
) -> tuple[int, int]:
    """
    Return the number of distinct terms and nonpositional postings.

    Each document is expected to already contain the tokens for the preprocessing stage being measured.
    """

    index: dict[str, set[int]] = {}

    for doc_id, tokens in documents:
        for term in tokens:
            if term not in index:
                index[term] = set()

            index[term].add(doc_id)

    distinc_terms = len(index)
    postings = sum(len(doc_ids) for doc_ids in index.values())

    return distinc_terms, postings


def process_unfiltered(
    tokens: list[str],
) -> list[str]:
    """Prepare tokens for the unfiltered experimental baseline."""

    return remove_punctuation(tokens)


def process_no_numbers(
    tokens: list[str],
) -> list[str]:
    """Remove punctuation and numeric terms."""

    tokens = remove_punctuation(tokens)

    return remove_numbers(tokens)


def process_case_folded(
    tokens: list[str],
) -> list[str]:
    """Remove punctuation and numbers, then case fold."""

    tokens = process_no_numbers(tokens)

    return case_fold(tokens)


def process_with_stop_words_removed(
    tokens: list[str],
    stop_words: set[str],
) -> list[str]:
    """Apply case folding and remove the supplied stop words."""

    tokens = process_case_folded(tokens)

    return remove_stop_words(tokens, stop_words)


def process_stemmed(
    tokens: list[str],
    stop_words: set[str],
) -> list[str]:
    """Apply preprocessing, stop-word removal, and stemming."""

    tokens = process_with_stop_words_removed(tokens, stop_words)

    return stem_tokens(tokens)