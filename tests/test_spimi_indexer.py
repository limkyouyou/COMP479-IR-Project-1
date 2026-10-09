from ir_project.naive_indexer import build_naive_index
from ir_project.spimi_indexer import build_spimi_index


def test_build_spimi_index():
    documents = [
        (10, ["Rain", "shadow", "rain"]),
        (20, ["Chaser", "rain"]),
    ]

    result = build_spimi_index(documents)

    assert result == {
        "rain": [10, 20],
        "shadow": [10],
        "chaser": [20],
    }


def test_spimi_does_not_duplicate_doc_ids():
    documents = [
        (10, ["rain", "rain", "rain"]),
        (20, ["rain"]),
    ]

    result = build_spimi_index(documents)

    assert result == {
        "rain": [10, 20],
    }


def test_spimi_normalizes_terms():
    documents = [
        (10, ["RAIN", "Chaser"]),
        (20, ["rain", "CHASER"]),
    ]

    result = build_spimi_index(documents)

    assert result == {
        "rain": [10, 20],
        "chaser": [10, 20],
    }


def test_spimi_matches_naive_index():
    documents = [
        (10, ["Rain", "shadow", "rain"]),
        (20, ["Chaser", "rain"]),
        (30, ["Shadow", "chaser", "rain"]),
    ]

    naive_index = build_naive_index(documents)
    spimi_index = build_spimi_index(documents)

    assert spimi_index == naive_index