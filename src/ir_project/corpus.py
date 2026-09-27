from collections.abc import Iterator

from nltk.corpus import reuters


def get_doc_id(file_id: str) -> int:
    """Extract the Reuters NEWID from an NLTK Reuters file ID."""

    return int(file_id.split("/")[-1])


def iter_documents() -> Iterator[tuple[int, list[str]]]:
    """Yield Reuters documents as (NEWID, tokens) pairs."""

    for file_id in reuters.fileids():
        doc_id = get_doc_id(file_id)
        tokens = list(reuters.words(file_id))

        yield doc_id, tokens