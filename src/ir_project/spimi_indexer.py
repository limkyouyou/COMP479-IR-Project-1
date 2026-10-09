from collections.abc import Iterable

from ir_project.naive_indexer import InvertedIndex
from ir_project.preprocessing import preprocess_tokens


def build_spimi_index(
    documents: Iterable[tuple[int, list[str]]],
) -> InvertedIndex:
    """Build an inverted index by directly appending DocIDs to postings lists."""

    index: InvertedIndex = {}

    for doc_id, tokens in documents:
        terms = preprocess_tokens(tokens)

        for term in terms:
            if term not in index:
                index[term] = []

            if not index[term] or index[term][-1] != doc_id:
                index[term].append(doc_id)

    return index