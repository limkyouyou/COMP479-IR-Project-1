from collections.abc import Iterator
from pathlib import Path
import re

from bs4 import BeautifulSoup, Tag


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "reuters21578"

REUTERS_FOOTER = re.compile(r"\s+Reuters?\s*$", re.IGNORECASE)


def remove_reuters_footer(text: str) -> str:
    """Remove a trailing Reuter/Reuters wire-service footer."""

    return REUTERS_FOOTER.sub("", text).strip()


def extract_document_text(document: Tag) -> str:
    """Extract indexable text from one <REUTERS> document."""

    text_element = document.find("text")

    if text_element is None:
        return ""

    text_type = text_element.get("type", "NORM").upper()

    if text_type == "BRIEF":
        title = text_element.find("title")

        if title is None:
            return ""

        return title.get_text(" ", strip=True)

    if text_type == "UNPROC":
        return text_element.get_text(" ", strip=True)

    # Normal Reuters article
    parts: list[str] = []

    title = text_element.find("title")
    body = text_element.find("body")

    if title is not None:
        parts.append(title.get_text(" ", strip=True))

    if body is not None:
        body_text = body.get_text(" ", strip=True)
        parts.append(remove_reuters_footer(body_text))

    return " ".join(parts).strip()


def iter_raw_document(
    data_dir: Path = DEFAULT_DATA_DIR,
) -> Iterator[tuple[int, str]]:
    """Yield Reuters document as (NEWID, raw article text)."""

    file_paths = sorted(data_dir.glob("reut2-*.sgm"))

    if not file_paths:
        raise FileNotFoundError(f"No Reuters SGML files found in {data_dir}")

    for file_path in file_paths:
        raw_sgml = file_path.read_text(encoding="latin-1")
        soup = BeautifulSoup(raw_sgml, "html.parser")

        for document in soup.find_all("reuters"):
            newid = document.get("newid")

            if newid is None:
                raise ValueError(f"Reuters document without NEWID in {file_path.name}")

            doc_id = int(newid)
            text = extract_document_text(document)

            yield doc_id, text