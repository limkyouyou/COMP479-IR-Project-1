from ir_project.compression import (
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


def transform_documents(transform):
    """Yield Reuters documents afterappying a token transformation."""

    for doc_id, tokens in iter_documents():
        yield doc_id, transform(tokens)


def print_row(
    name: str,
    terms: str,
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


if __name__ == "__main__":
    main()