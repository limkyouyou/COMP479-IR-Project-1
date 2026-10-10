from time import perf_counter

from ir_project.compression import (
    build_index_from_documents,
    compute_index_statistics,
    process_case_folded,
    process_no_numbers,
    process_stemmed,
    process_unfiltered,
    process_with_stop_words_removed,
    rank_stop_words,
    select_stop_words,
)
from ir_project.corpus import iter_documents
from ir_project.naive_indexer import (
    build_inverted_index,
    build_naive_index,
    sort_and_deduplicate,
)
from ir_project.preprocessing import preprocess_tokens
from ir_project.query_processor import (
    process_query,
    parse_query,
    and_query,
)
from ir_project.spimi_indexer import build_spimi_index


PAIR_LIMIT = 10_000
REPEATS = 20
QUERIES = [
    "stock",
    "market",
    "exchange",
    "stock AND market",
    "share AND equity",
    "portfolio AND trade",
]


def run_query(index, query: str):
    """Run a query and return its results and execution time."""

    start = perf_counter()
    results = process_query(index, query)
    elapsed = perf_counter() - start

    return results, elapsed


def print_section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def collect_pairs(limit: int) -> list[tuple[str, int]]:
    """Collect normalizes term-DocID pairings for the timing experiments."""
    pairs: list[tuple[str, int]] = []

    for doc_id, tokens in iter_documents():
        terms = preprocess_tokens(tokens)

        for term in terms:
            pairs.append((term, doc_id))

            if len(pairs) == limit:
                return pairs

    return pairs


def build_naive_from_pairs(pairs: list[tuple[str, int]]) -> dict[str, list[int]]:
    """Build an index using naive sorting and deduplication."""

    pairs = pairs.copy()
    unique_pairs = sort_and_deduplicate(pairs)

    return build_inverted_index(unique_pairs)


def build_spimi_from_pairs(pairs: list[tuple[str, int]]) -> dict[str, list[int]]:
    """Build an index by directly appending DocIDs."""

    index: dict[str, list[int]] = {}

    for term, doc_id in pairs:
        if term not in index:
            index[term] = []

        if not index[term] or index[term][-1] != doc_id:
            index[term].append(doc_id)

    return index


def compressed_documents(stor_words: set[str]):
    """Yield reuters documents using the final compression rules."""

    for doc_id, tokens in iter_documents():
        yield doc_id, process_stemmed(tokens, stor_words)


def process_compressed_query(
    index: dict[str, list[int]],
    query: str,
    stop_words: set[str],
) -> list[int]:
    """Process a query using the same rules as the compressed index."""

    terms = parse_query(query)

    compressed_terms = process_stemmed(terms, stop_words)

    return and_query(index, compressed_terms)


def transform_documents(transform):
    """Yield Reuters documents after appying a token transformation."""

    for doc_id, tokens in iter_documents():
        yield doc_id, transform(tokens)


def print_row(
    name: str,
    terms: int,
    postings: int,
    reference_terms: int,
    reference_postings: int,
    base_terms: int, 
    base_postings: int,
) -> None:
    term_delta = percent_change(terms, reference_terms)
    term_total = percent_change(terms, base_terms)

    postings_delta = percent_change(postings, reference_postings)
    postings_total = percent_change(postings, base_postings)

    print(
        f"{name:<18}"
        f"{terms:>12,}"
        f"{term_delta:>9.2f}%"
        f"{term_total:>9.2f}%"
        f"{postings:>15,}"
        f"{postings_delta:>9.2f}%"
        f"{postings_total:>9.2f}%"
    )


def percent_change(
    value: int,
    reference: int,
) -> float:

    return ((value - reference) / reference) * 100


def main():
    print("=" * 60)
    print("COMP 479 - Information Retrieval Project Demo")
    print("=" * 60)

    # Subporject I - Naive Indexer
    print_section("Subproject I - Naive Indexer")

    print("Building naive Reuters index...")
    start = perf_counter()
    naive_index = build_naive_index(iter_documents())
    naive_build_time = perf_counter() - start

    print()
    print(f"Unique terms: {len(naive_index):,}")
    print(f"Build time: {naive_build_time:.4f} seconds")

    sample_terms = ["stock", "market", "exchange"]

    print("\nSample document frequencies:")

    for term in sample_terms:
        postings = naive_index.get(term, [])
        print(f"  {term:<10} {len(postings):,}")

    # Subproject II - Query Processing
    print_section("Subproject II - Query Processing")
    print("Supported query examples:")
    print("  Single-term query: stock")
    print("  AND query:         stock AND market")
    print("  EXIT demo:         exit query")

    while True:
        query = input("\nQuery: ").strip()

        if query.lower() == "exit query":
            break

        if not query:
            continue

        naive_results, naive_query_time = run_query(naive_index, query)

        print("\nQuery Results")
        print("-" * 60)

        print(f"Documents found: {len(naive_results):,}")
        print(f"First 20 DocIDs: {naive_results[:20]}")

        print()
        print(f"Naive query time: {naive_query_time:.8f} seconds")

    # Subproject IIIa - Compression Table
    print_section("Subproject IIIa - Compression Table")
    print("Ranking Reuters stop words...")
    ranked_stop_words = rank_stop_words(iter_documents())

    stop_30 = select_stop_words(ranked_stop_words, 30)
    stop_150 = select_stop_words(ranked_stop_words, 150)

    print("\nTop 30 Reuters stop words:")
    print([term for term, _ in ranked_stop_words[:30]])

    print("\nComputing compression statistics...\n")

    unfiltered = compute_index_statistics(
        transform_documents(process_unfiltered)
    )

    no_numbers = compute_index_statistics(
        transform_documents(process_no_numbers)
    )

    case_folded = compute_index_statistics(
        transform_documents(process_case_folded)
    )

    stop_30_stats = compute_index_statistics(
        transform_documents(
            lambda tokens: process_with_stop_words_removed(tokens, stop_30)
        )
    )

    stop_150_stats = compute_index_statistics(
        transform_documents(
            lambda tokens: process_with_stop_words_removed(tokens, stop_150)
        )
    )

    stemmed = compute_index_statistics(
        transform_documents(
            lambda tokens: process_stemmed(tokens, stop_150)
        )
    )

    base_terms, base_postings = unfiltered

    print(
        f"{'Stage':<18}"
        f"{'Terms':>12}"
        f"{'Δ%':>10}"
        f"{'T%':>10}"
        f"{'Postings':>15}"
        f"{'Δ%':>10}"
        f"{'T%':>10}"
    )
    print("-" * 85)

    print(
        f"{'Unfiltered':<18}"
        f"{base_terms:>12,}"
        f"{'—':>10}"
        f"{'—':>10}"
        f"{base_postings:>15,}"
        f"{'—':>10}"
        f"{'—':>10}"
    )

    stages = [
        ("No numbers", no_numbers, unfiltered),
        ("Case folding", case_folded, no_numbers),
        ("30 stop words", stop_30_stats, case_folded),
        ("150 stop words", stop_150_stats, case_folded),
        ("Stemming", stemmed, stop_150_stats),
    ]

    for name, (terms, postings), (ref_terms, ref_postings) in stages:
        print_row(
            name,
            terms,
            postings,
            ref_terms,
            ref_postings,
            base_terms,
            base_postings,
        )

    # Subproject IIIb - Compare retrieval result
    print_section("Subproject IIIb - Compare retrieval result")

    print("Building compressed index...")
    compressed_index = build_index_from_documents(compressed_documents(stop_150))

    print()
    print(f"Six sample queries: {QUERIES}")

    print()
    print(
        f"{'Query':<25}"
        f"{'Base':>10}"
        f"{'Compressed':>15}"
        f"{'Difference':>15}"
    )
    print("-" * 65)

    for query in QUERIES:
        base_result = process_query(naive_index, query)

        compressed_result = process_compressed_query(compressed_index, query, stop_150)

        difference = len(compressed_result) - len(base_result)

        print(
            f"{query:<25}"
            f"{len(base_result):>10,}"
            f"{len(compressed_result):>15,}"
            f"{difference:>+15,}"
        )

    # Subproject IV - SPIMI
    print_section("Subproject IV - SPIMI")
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

    print()
    print("=" * 60)
    print("Demo finished.")
    print("=" * 60)

    
if __name__ == "__main__":
    main()