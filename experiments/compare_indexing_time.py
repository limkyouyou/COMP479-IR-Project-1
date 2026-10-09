from time import perf_counter

from ir_project.corpus import iter_documents
from ir_project.naive_indexer import (
    build_inverted_index,
    sort_and_deduplicate,
)
from ir_project.preprocessing import preprocess_tokens


PAIR_LIMIT = 10_000
REPEATS = 20


def collect_pairs(limit: int) -> list[tuple[str, int]]:
    """Collect the first requested number of normalized term-DocID pairings."""

    pairs: list[tuple[str, int]] = []

    for doc_id, tokens in iter_documents():
        terms = preprocess_tokens(tokens)

        for term in terms:
            pairs.append((term, doc_id))

            if len(pairs) == limit:
                return pairs

    return pairs


def build_naive_from_pairs(
    pairs: list[tuple[str, int]],
) -> dict[str, list[int]]:
    """Build an index using sorting and deduplication."""

    pairs = pairs.copy()

    unique_pairs = sort_and_deduplicate(pairs)

    return build_inverted_index(unique_pairs)


def build_spimi_from_pairs(
    pairs: list[tuple[str, int]],
) -> dict[str, list[int]]:
    """Build an index by directly appending DocIDs to postings lists."""

    index: dict[str, list[int]] = {}

    for term, doc_id in pairs:
        if term not in index:
            index[term] = []

        if not index[term] or index[term][-1] != doc_id:
            index[term].append(doc_id)

    return index


def main():
    print(f"Collecting {PAIR_LIMIT:,} term-DocID pairings...")
    pairs = collect_pairs(PAIR_LIMIT)

    print(f"Pairings collected: {len(pairs):,}")

    naive_times = []

    for _ in range(REPEATS):
        naive_start = perf_counter()
        naive_index = build_naive_from_pairs(pairs)
        naive_times.append(perf_counter() - naive_start)

    spimi_times = []

    for _ in range(REPEATS):
        spimi_start = perf_counter()
        spimi_index = build_spimi_from_pairs(pairs)
        spimi_times.append(perf_counter() - spimi_start)

    naive_average = sum(naive_times) / REPEATS
    spimi_average = sum(spimi_times) / REPEATS

    print()
    print(f"Naive average: {naive_average:.6f} seconds")
    print(f"SPIMI average: {spimi_average:.6f} seconds")

    print()
    print(f"Indexes match: {naive_index == spimi_index}")


if __name__ == "__main__":
    main()