from ir_project.corpus import iter_documents
from ir_project.naive_indexer import build_naive_index, InvertedIndex
from ir_project.query_processor import parse_query, process_query


SINGLE_QUERIES = [
    "oil",
    "trade",
    "market",
]

AND_QUERIES = [
    "oil AND market",
    "trade AND japan",
    "bank AND dollar",
]


def expected_result(
    index: InvertedIndex,
    query: str,
) -> list[int]:
    """Compute a reference result using Python set intersections."""

    terms = parse_query(query)

    if not terms:
        return []

    result = set(index.get(terms[0], []))

    for term in terms[1:]:
        result &= set(index.get(term, []))

    return sorted(result)


def run_query(
    index: InvertedIndex,
    query: str,
) -> list[int]:
    result = process_query(index, query)
    expected = expected_result(index, query)

    assert result == expected

    print(f"Query: {query}")
    print(f"Documents found: {len(result)}")
    print(f"First 20 DocIDs: {result[:20]}")
    print("Validation: PASS")
    print()


def main():
    print("Building Reuters naive index...")
    index = build_naive_index(iter_documents())

    print("\nSingle-term queries\n")

    for query in SINGLE_QUERIES:
        run_query(index, query)

    print("AND queries\n")

    for query in AND_QUERIES:
        run_query(index, query)


if __name__ == "__main__":
    main()