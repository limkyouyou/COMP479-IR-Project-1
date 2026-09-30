from ir_project.corpus import iter_documents
from ir_project.naive_indexer import build_naive_index


def main():
    index = build_naive_index(iter_documents())

    terms = list(index)

    longest_terms = sorted(terms, key=len, reverse=True)[:30]

    apostrophe_terms = [term for term in terms if "'" in term][:30]

    period_terms = [term for term in terms if "." in term][:30]

    numeric_terms = [term for term in terms if any(char.isdigit() for char in term)][:30]

    print(f"Total unique terms: {len(terms):,}")

    print("\nLongest terms:")
    for term in longest_terms:
        print(repr(term))

    print("\nTerms containing apostrophes:")
    for term in apostrophe_terms:
        print(repr(term))

    print("\nTerms containing periods:")
    for term in period_terms:
        print(repr(term))

    print("\nTerms containing number:")
    for term in numeric_terms:
        print(repr(term))


if __name__ == "__main__":
    main()