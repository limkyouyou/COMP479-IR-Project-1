from time import perf_counter

from ir_project.corpus import iter_documents
from ir_project.naive_indexer import build_naive_index
from ir_project.spimi_indexer import build_spimi_index


def main():
    print("Building naive Reuters index...")
    naive_start = perf_counter()
    naive_index = build_naive_index(iter_documents())
    naive_time = perf_counter() - naive_start

    print("Building SPIMI Reuters index...")
    spimi_start = perf_counter()
    spimi_index = build_spimi_index(iter_documents())
    spimi_time = perf_counter() - spimi_start

    print()
    print(f"Naive unique terms: {len(naive_index):,}")
    print(f"SPIMI unique terms: {len(spimi_index):,}")

    print(f"Naive build time: {naive_time:.4f} seconds")
    print(f"SPIMI build time: {spimi_time:.4f} seconds")

    print()
    print(f"Indexes match: {naive_index == spimi_index}")

    sample_terms = ["oil", "trade", "market"]

    for term in sample_terms:
        print()
        print(f"Term: {term}")
        print(f"Naive df: {len(naive_index.get(term, []))}")
        print(f"SPIMI df: {len(spimi_index.get(term, []))}")


if __name__ == "__main__":
    main()