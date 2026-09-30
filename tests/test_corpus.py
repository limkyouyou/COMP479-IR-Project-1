from pathlib import Path

from bs4 import BeautifulSoup

from ir_project.corpus import (
    extract_document_text,
    iter_documents,
    iter_raw_documents,
    remove_reuters_footer,
)


def make_document(sgml: str):
    soup = BeautifulSoup(sgml, "html.parser")
    return soup.find("reuters")


def test_remove_reuters_footer():
    text = "Oil prices increased sharply today. Reuter"

    result = remove_reuters_footer(text)

    assert result == "Oil prices increased sharply today."


def test_extract_normal_document():
    document = make_document(
        """
        <REUTERS NEWID="1">
            <TEXT>
                <TITLE>Oil Prices Rise</TITLE>
                <DATELINE>NEW YORK, Feb 26 -</DATELINE>
                <BODY>Oil prices increased. Reuter</BODY>
            </TEXT>
        </REUTERS>
        """
    )

    result = extract_document_text(document)

    assert result == (
        "Oil Prices Rise "
        "Oil prices increased."
    )


def test_extract_brief_document():
    document = make_document(
        """
        <REUTERS NEWID="30">
            <TEXT TYPE="BRIEF">
                <TITLE>MARKET PRICES RISE</TITLE>
                Blah blah blah.
            </TEXT>
        </REUTERS>
        """
    )

    result = extract_document_text(document)

    assert result == "MARKET PRICES RISE"


def test_extract_unprocessed_document():
    document = make_document(
        """
        <REUTERS NEWID="99">
            <TEXT TYPE="UNPROC">
                FEDERAL RESERVE WEEKLY REPORT
                Bank borrowings increased.
            </TEXT>
        </REUTERS>
        """
    )

    result = extract_document_text(document)

    assert "FEDERAL RESERVE WEEKLY REPORT" in result
    assert "Bank borrowings increased." in result


def test_iter_raw_documents_reads_reuters_files():
    documents = iter_raw_documents()

    doc_id, text = next(documents)

    assert doc_id == 1
    assert isinstance(text, str)
    assert len(text) > 0


def test_iter_documents_tokenizes_text():
    documents = iter_documents()

    doc_id, tokens = next(documents)

    assert doc_id == 1
    assert isinstance(tokens, list)
    assert len(tokens) > 0
    assert all(isinstance(token, str) for token in tokens)


def test_first_document_contains_expected_terms():
    doc_id, tokens = next(iter_documents())

    assert doc_id == 1
    assert "BAHIA" in tokens
    assert "COCOA" in tokens
    assert "REVIEW" in tokens