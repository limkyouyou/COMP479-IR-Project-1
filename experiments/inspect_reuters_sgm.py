from pathlib import Path

from bs4 import BeautifulSoup


DATA_DIR = Path("data/reuters21578")


def find_document_type(text_type: str):
    for file_path in sorted(DATA_DIR.glob("reut2-*.sgm")):
        raw_sgml = file_path.read_text(encoding="latin-1")
        soup = BeautifulSoup(raw_sgml, "html.parser")

        for document in soup.find_all("reuters"):
            text_element = document.find("text")

            if text_element is not None and text_element.get("type") == text_type:
                doc_id = int(document["newid"])
                document_text = text_element.get_text(" ", strip=True)

                return file_path.name, doc_id, document_text

    return None




def main():
    for text_type in ["BRIEF", "UNPROC"]:
        result = find_document_type(text_type)

        print(f"\n{text_type}")
        print("=" * 60)

        if result is None:
            print("No document found.")
            continue

        file_name, doc_id, document_text = result

        print(f"File: {file_name}")
        print(f"NEWID: {doc_id}")
        print()
        print("TEXT:")
        print(document_text[:1000])


if __name__ == "__main__":
    main()