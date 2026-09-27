from ir_project.preprocessing import preprocess_tokens


def test_preprocess_tokens_lowercase_terms():
    tokens = ["CHASING", "Shadows", "in", "tHe", "raiN"]

    result = preprocess_tokens(tokens)

    assert result == ["chasing", "shadows", "in", "the", "rain"]


def test_preprocessing_tokens_removes_punctuation():
    tokens = ["CHASING", "--", "Shadows", ",", "in", ".", "tHe", "raiN"]

    result = preprocess_tokens(tokens)

    assert result == ["chasing", "shadows", "in", "the", "rain"]


def test_preprocess_tokens_keeps_numbers():
    tokens = ["007", "shadows", "1989"]

    result = preprocess_tokens(tokens)

    assert result == ["007", "shadows", "1989"]