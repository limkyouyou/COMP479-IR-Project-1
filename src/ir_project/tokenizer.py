import re


TOKEN_PATTERN = re.compile(
    r"""
    (?:[A-Za-z]\.)+[A-Za-z]\.?      # abbreviations: U.S., e.g.
    |
    [A-Za-z]+(?:'[A-Za-z]+)+        # contractions/possessives: can't, you're, company's
    |
    \d{1,3}(?:,\d{3})+(?:\.\d+)?    # comma numbers: 1,850 or 1,850.50
    |
    \d+\.\d+                        # decimals: 3.88
    |
    [A-Za-z0-9]+                    # Normal words and remaining numbers
    """,
    re.VERBOSE,
)


def tokenize_text(text: str) -> list[str]:
    """Tokenize Reuters article text using the project's IR rules."""

    # Split hyphenated terms into their components.
    text = text.replace("-", " ")

    tokens = TOKEN_PATTERN.findall(text)

    # Remove formatting commas from numeric token.
    return [token.replace(",", "") if any(char.isdigit() for char in token) else token for token in tokens]