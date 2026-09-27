from collections.abc import Iterable

from ir_project.preprocessing import preprocess_tokens


TermDocPair = tuple[str, int]
InvertedIndex = dict[str, list[int]]


def generate_term_doc_pairs(
    doc_id: int,
    tokens: list[str],
) -> list[TermDocPair]:
    """Generate (term, docID) pair for one document."""

    terms = preprocess_tokens(tokens)

    return [(term, doc_id) for term in terms]


def sort_and_deduplicate(
    pairs: list[TermDocPair],
) -> list[TermDocPair]:
    """Sort term-document pairs and remove duplicate pairs."""

    pairs.sort()

    unique_pairs = []

    for pair in pairs:
        if not unique_pairs or pair != unique_pairs[-1]:
            unique_pairs.append(pair)

    return unique_pairs


def build_inverted_index(
    pairs: list[TermDocPair],
) -> InvertedIndex:
    """Create an inverted index from sorted unique term-document pairs."""

    index: InvertedIndex = {}

    for term, doc_id in pairs:
        if term not in index:
            index[term] = []

        index[term].append(doc_id)

    return index


def build_naive_index(
    documents: Iterable[tuple[int, list[str]]],
) -> InvertedIndex:
    """Build a naive inverted index from a collection of documents."""

    pairs: list[TermDocPair] = []

    for doc_id, tokens in documents:
        pairs.extend(generate_term_doc_pairs(doc_id, tokens))

    unique_pairs = sort_and_deduplicate(pairs)

    return build_inverted_index(unique_pairs)