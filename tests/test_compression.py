from ir_project.compression import (
    case_fold,
    is_number_token,
    rank_stop_words,
    remove_numbers,
    remove_stop_words,
    select_stop_words,
    stem_tokens,
)


def test_rank_stop_words_by_frequency():
    documents = [
        (1, ["The", "the", "and", "market"]),
        (2, ["the", "AND", "of", "trade"]),
        (3, ["to", "oil"]),
    ]

    result = rank_stop_words(documents)

    assert result[:4] == [
        ("the", 3),
        ("and", 2),
        ("of", 1),
        ("to", 1),
    ]


def test_rank_stop_words_breaks_ties_alphabetically():
    documents = [
        (1, ["to", "of"]),
    ]

    result = rank_stop_words(documents)

    assert result[:2] == [
        ("of", 1),
        ("to", 1),
    ]


def test_select_stop_words():
    ranked_stop_words = [
        ("the", 10),
        ("and", 8),
        ("of", 6),
        ("to", 4),
    ]

    result = select_stop_words(ranked_stop_words, 3)

    assert result == {"the", "and", "of"}


def test_smaller_stop_list_is_subset_of_larger():
    ranked_stop_words = [
        ("the", 10),
        ("and", 8),
        ("of", 6),
        ("to", 4),
    ]

    stop_2 = select_stop_words(ranked_stop_words, 2)
    stop_4 = select_stop_words(ranked_stop_words, 4)

    assert stop_2.issubset(stop_4)


def test_is_number_token():
    assert is_number_token("1987")
    assert is_number_token("3.88")
    assert is_number_token("1850.50")

    assert not is_number_token("g7")
    assert not is_number_token("u.s.")


def test_remove_numbers():
    tokens = [
        "oil",
        "1987",
        "3.88",
        "1850.50",
        "market",
        "g7",
    ]

    result = remove_numbers(tokens)

    assert result == ["oil", "market", "g7"]


def test_case_fold():
    tokens = [
        "OIL",
        "Market",
        "TrAdE",
    ]

    result = case_fold(tokens)

    assert result == ["oil", "market", "trade"]


def test_remove_stop_words():
    tokens = [
        "the",
        "oil",
        "and",
        "market",
        "of",
        "trade",
    ]
    stop_words = {
        "the",
        "and",
        "of",
    }

    result = remove_stop_words(tokens, stop_words)

    assert result == ["oil", "market", "trade"]


def test_stem_tokens():
    tokens = [
        "markets",
        "marketing",
        "connected",
        "connections",
    ]

    result = stem_tokens(tokens)

    assert result == [
        "market",
        "market",
        "connect",
        "connect",
    ]