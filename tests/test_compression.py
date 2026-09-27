from ir_project.compression import rank_stop_words, select_stop_words


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