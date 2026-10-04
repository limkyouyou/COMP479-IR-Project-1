from ir_project.naive_indexer import InvertedIndex
from ir_project.preprocessing import preprocess_tokens
from ir_project.tokenizer import tokenize_text


def parse_query(
    query: str,
) -> list[str]:
    """Tokenize and normalize a raw query string."""

    tokens = tokenize_text(query)

    # Remove Boolean AND operator.
    tokens = [token for token in tokens if token != "AND"]

    return preprocess_tokens(tokens)


def process_query(
    index: InvertedIndex,
    query: str,
) -> list[int]:
    """Process a raw single-term or AND query."""

    terms = parse_query(query)

    if not terms:
        return []

    if len(terms) == 1:
        return single_term_query(index, terms[0])

    return and_query(index, terms)


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