from ir_project.naive_indexer import (
    build_inverted_index,
    build_naive_index,
    generate_term_doc_pairs,
    sort_and_deduplicate,
)


def test_generate_term_doc_pairs():
    tokens = ["Rain", "chaser", "rain", "."]

    result = generate_term_doc_pairs(10, tokens)

    assert result == [
        ("rain", 10),
        ("chaser", 10),
        ("rain", 10),
    ]


def test_sort_and_deduplicate():
    pairs = [
        ("rain", 20),
        ("shadow", 10),
        ("rain", 10),
        ("rain", 10),
        ("chaser", 20),
    ]

    result = sort_and_deduplicate(pairs)

    assert result == [
        ("chaser", 20),
        ("rain", 10),
        ("rain", 20),
        ("shadow", 10),
    ]


def test_build_inverted_index():
    pairs = [
        ("chaser", 20),
        ("rain", 10),
        ("rain", 20),
        ("shadow", 10),
    ]

    result = build_inverted_index(pairs)

    assert result == {
        "chaser": [20],
        "rain": [10, 20],
        "shadow": [10],
    }


def test_build_naive_index():
    documents = [
        (10, ["Rain", "shadow", "rain"]),
        (20, ["Chaser", "rain", "."]),
    ]

    result = build_naive_index(documents)

    assert result == {
        "chaser": [20],
        "rain": [10, 20],
        "shadow": [10],
    }