from ir_project.naive_indexer import InvertedIndex
from ir_project.preprocessing import preprocess_tokens


def single_term_query(
    index: InvertedIndex,
    term: str,
) -> list[int]:
    """Return the postings list for a single query term."""

    terms = preprocess_tokens([term])
    
    if not terms:
        return []

    normalized_term = terms[0]

    return index.get(normalized_term, [])


def intersect_postings(
    postings1: list[int],
    postings2: list[int],
) -> list[int]:
    """Intersect two sorted postings lists."""

    result = []

    i = 0
    j = 0

    while i < len(postings1) and j < len(postings2):
        if postings1[i] == postings2[j]:
            result.append(postings1[i])
            i += 1
            j += 1
        
        elif postings1[i] < postings2[j]:
            i += 1
        
        else:
            j += 1

    return result


def and_query(
    index: InvertedIndex,
    terms: list[str],
) -> list[int]:
    """Return documents containing all query terms."""

    if not terms:
        return []

    normalized_terms = preprocess_tokens(terms)

    if not normalized_terms:
        return []

    result = index.get(normalized_terms[0], [])

    for term in normalized_terms[1:]:
        postings = index.get(term, [])
        result = intersect_postings(result, postings)

        if not result:
            break

    return result