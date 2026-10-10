from ir_project.compression import (
    build_index_from_documents,
    process_stemmed,
    rank_stop_words,
    select_stop_words,
)
from ir_project.corpus import iter_documents
from ir_project.naive_indexer import build_naive_index
from ir_project.query_processor import (
    and_query,
    parse_query,
    process_query,
)


QUERIES = [
    "stock",
    "market",
    "exchange",
    "stock AND market",
    "share AND equity",
    "portfolio AND trade",
]


def compressed_documents(stop_words: set[str]):
    """Yield Reuters documents using the final compression rules."""

    for doc_id, tokens in iter_documents():
        yield doc_id, process_stemmed(tokens, stop_words)


def process_compressed_query(
    index: dict[str, list[int]],
    query: str,
    stop_words: set[str],
) -> list[int]:
    """Process a query using the same rules as the compressed index."""

    terms = parse_query(query)

    compressed_terms = process_stemmed(terms, stop_words)

    return and_query(index, compressed_terms)


def main():
    print("Ranking stop words...")
    ranked = rank_stop_words(iter_documents())
    stop_150 = select_stop_words(ranked, 150)

    print("Building base index...")
    base_index = build_naive_index(iter_documents())

    print("Building compressed index...")
    compressed_index = build_index_from_documents(compressed_documents(stop_150))

    print()
    print(
        f"{'Query':<25}"
        f"{'Base':>10}"
        f"{'Compressed':>15}"
        f"{'Difference':>15}"
    )
    print("-" * 65)

    for query in QUERIES:
        base_result = process_query(base_index, query)

        compressed_result = process_compressed_query(compressed_index, query, stop_150)

        difference = len(compressed_result) - len(base_result)

        print(
            f"{query:<25}"
            f"{len(base_result):>10,}"
            f"{len(compressed_result):>15,}"
            f"{difference:>+15,}"
        )


if __name__ == "__main__":
    main()