from time import perf_counter

from nltk.corpus import reuters

from ir_project.corpus import iter_documents
from ir_project.naive_indexer import build_naive_index


def main():
    print(f"Reuters documents: {len(reuters.fileids())}")

    start = perf_counter()

    index = build_naive_index(iter_documents())

    elapsed = perf_counter() - start

    for postings in index.values():
        assert postings == sorted(set(postings))

    print(f"Unique terms: {len(index)}")
    print(f"Build time: {elapsed:.4f} seconds")

    sample_terms = ["oil", "trade", "market"]

    for term in sample_terms:
        postings = index.get(term, [])

        print()
        print(f"Term: {term}")
        print(f"Document frequency: {len(postings)}")
        print(f"First 20 DocIDs: {postings[:20]}")


if __name__ == "__main__":
    main()