from ir_project.corpus import get_doc_id, iter_documents


def test_get_doc_id():
    assert get_doc_id("test/14826") == 14826
    assert get_doc_id("training/1") == 1


def test_iter_documents():
    documents = iter_documents()

    doc_id, tokens = next(documents)

    assert isinstance(doc_id, int)
    assert isinstance(tokens, list)
    assert len(tokens) > 0