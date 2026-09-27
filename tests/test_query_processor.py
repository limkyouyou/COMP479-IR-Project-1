from ir_project.query_processor import (
    and_query,
    intersect_postings,
    single_term_query,
)


TEST_INDEX = {
    "chaser": [20, 30, 50],
    "rain": [10, 20, 30, 40],
    "shadow": [10, 30, 40, 50],
}


def test_single_term_query():
    result = single_term_query(TEST_INDEX, "rain")

    assert result == [10, 20, 30, 40]


def test_single_term_query_normalizes_case():
    result = single_term_query(TEST_INDEX, "RAIN")

    assert result == [10, 20, 30, 40]


def test_single_term_query_missing_term():
    result = single_term_query(TEST_INDEX, "sun")

    assert result == []


def test_intersect_postings():
    postings1 = [1, 4, 7, 10, 15]
    postings2 = [2, 4, 7, 12, 15]

    result = intersect_postings(postings1, postings2)

    assert result == [4, 7, 15]


def test_and_query_two_terms():
    result = and_query(TEST_INDEX, ["rain", "shadow"])

    assert result == [10, 30, 40]


def test_and_query_multiple_terms():
    result = and_query(TEST_INDEX, ["rain", "shadow", "chaser"])

    assert result == [30]


def test_and_query_missing_term():
    result = and_query(TEST_INDEX, ["rain", "sun"])

    assert result == []