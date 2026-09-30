from ir_project.tokenizer import tokenize_text


def test_tokenize_normal_words():
    text = "Oil prices rise"

    result = tokenize_text(text)

    assert result == ["Oil", "prices", "rise"]


def test_tokenize_discards_standalone_punctuation():
    text = 'Oil, prices. "Rise!"'

    result = tokenize_text(text)

    assert result == ["Oil", "prices", "Rise"]


def test_tokenzie_preserves_contractions():
    text = "can't you're won't"

    result = tokenize_text(text)

    assert result == ["can't", "you're", "won't"]


def test_tokenize_preserves_possessives():
    text = "company's market's"

    result = tokenize_text(text)

    assert result == ["company's", "market's"]


def test_tokenize_splits_hyphenated_words():
    text = "oil-price long-term"

    result = tokenize_text(text)

    assert result == ["oil", "price", "long", "term"]


def test_tokenize_preserves_decimal_numbers():
    text = "The price is 3.88 dollars."

    result = tokenize_text(text)

    assert result == ["The", "price", "is", "3.88", "dollars"]


def test_tokenize_normalizes_comma_numbers():
    text = "Sales reached 1,850 units."

    result = tokenize_text(text)

    assert result == ["Sales", "reached", "1850", "units"]


def test_tokenize_normalizes_comma_decimal_numbers():
    text = "Revenue was 7,850.75 dollars."

    result = tokenize_text(text)

    assert result == ["Revenue", "was", "7850.75", "dollars"]


def test_tokenize_preserves_abbreviations():
    text = "U.S. markets rose."

    result = tokenize_text(text)

    assert result == ["U.S.", "markets", "rose"]


def test_tokenize_date_components():
    text = "February 22"

    result = tokenize_text(text)

    assert result == ["February", "22"]


def test_tokenize_hyphenated_date_components():
    text = "26-FEB-1987"

    result = tokenize_text(text)

    assert result == ["26", "FEB", "1987"]


def test_tokenize_keeps_standalone_numbers():
    text = "The company sold 15 units in 1987."

    result = tokenize_text(text)

    assert result == ["The", "company", "sold", "15", "units", "in", "1987"]


def test_tokenize_financial_text():
    text = "U.S. oil-price rose to 1,850.50 dlrs on Feb. 26."

    result = tokenize_text(text)

    assert result == ["U.S.", "oil", "price", "rose", "to", "1850.50", "dlrs", "on", "Feb", "26"]