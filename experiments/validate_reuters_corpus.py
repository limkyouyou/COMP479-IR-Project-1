from ir_project.corpus import iter_raw_documents


def main():
    documents = list(iter_raw_documents())

    doc_ids = [doc_id for doc_id, _ in documents]
    unique_ids = set(doc_ids)

    empty_documents = [doc_id for doc_id, text in documents if not text.strip()]

    expected_ids = set(range(1, 21579))
    missing_ids = expected_ids - unique_ids

    print(f"Documents parsed: {len(documents):,}")
    print(f"Unique NEWIDs: {len(unique_ids):,}")
    print(f"Empty extracted documents: {len(empty_documents):,}")
    print(f"Missing expected NEWIDs: {len(missing_ids):,}")

    if empty_documents:
        print(f"First empty NEWIDs: {empty_documents[:20]}")

    if missing_ids:
        print(f"First missing NEWIDs: {sorted(missing_ids)[:20]}")


if __name__ == "__main__":
    main()