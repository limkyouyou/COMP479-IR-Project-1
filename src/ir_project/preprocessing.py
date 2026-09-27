def preprocess_tokens(tokens: list[str]) -> list[str]:
    """
    Normalize tokens for indexing.

    Convers tokens to lowercase and removes tokens that contain no alphanumeric characters.
    """

    return [token.lower() for token in tokens if any(char.isalnum() for char in token)]