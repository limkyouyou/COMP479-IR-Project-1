# COMP 479 - Information Retrieval Project 1

This project implements indexing and Boolean retrieval techniques on the Reuters-21578 document collection.

The project includes:

- Subproject I: Naive inverted indexing
- Subproject II: Single-term and Boolean AND queries
- Subproject III: Lossy dictionary compression experiments
- Subproject IV: Single-Pass In-Memory Indexing (SPIMI)
- Unit tests and additional corpus/tokenization validation
- Interactive demonstration script

## Requirements

- Python 3
- NLTK
- Beautiful Soup 4
- pytest

Install the required Python packages with:

```bash
pip install -r requirements.txt
```

The NLTK English stop-word corpus is also required for the compression experiment.

Run the following once after installing NLTK:

```bash
python -c "import nltk; nltk.download('stopwords')"
```

## Reuters-21578 Dataset

The project uses the original Reuters-21578 SGML distribution.

The dataset is intentionally not included in the Git repository.

Download and extract the Reuters-21578 files, then place the SGML files in:

```text
data/reuters21578/
```

The directory should contain:

```text
reut2-000.sgm
reut2-001.sgm
...
reut2-021.sgm
```

The parser reads all 22 SGML files directly and uses the `NEWID` attribute of each Reuters document as its DocID.

The complete collection contains:

```text
21,578 documents
```

## Running the Demo

The main demonstration file is:

```text
demo/demo.py
```

### Windows PowerShell

From the project root:

```powershell
$env:PYTHONPATH="src"
python .\demo\demo.py
```

### Linux/macOS

```bash
PYTHONPATH=src python demo/demo.py
```

The demo covers all four subprojects:

1. Builds the naive Reuters inverted index.
2. Allows interactive single-term and AND queries.
3. Runs the dictionary compression experiment and compressed-query comparison.
4. Builds the full SPIMI index and compares naive and SPIMI indexing time.

During the query demonstration, enter:

```text
exit query
```

to leave query mode and continue to the next subproject.

Example queries:

```text
stock
market
stock AND market
share AND equity
```

## Running the Tests

Run all unit tests from the project root:

```bash
pytest
```

The tests cover:

- Reuters document extraction
- Tokenization
- Preprocessing
- Naive index construction
- Query processing
- Dictionary compression
- SPIMI indexing
- Equality between naive and SPIMI indexes on test data

## Main Project Files

```text
src/ir_project/
│
├── corpus.py
│   Parses the Reuters-21578 SGML files and extracts indexable text.
│
├── tokenizer.py
│   Implements the custom Reuters tokenization rules.
│
├── preprocessing.py
│   Performs normalization used by the base index.
│
├── naive_indexer.py
│   Implements the naive term-DocID pair indexing algorithm.
│
├── query_processor.py
│   Implements single-term and Boolean AND queries.
│
├── compression.py
│   Implements the lossy dictionary compression techniques.
│
└── spimi_indexer.py
    Implements Single-Pass In-Memory Indexing (SPIMI).
```

## Experiment Files

```text
experiments/
│
├── run_naive_reuters.py
│   Builds and inspects the full naive Reuters index.
│
├── run_sample_queries.py
│   Runs and validates the six sample queries.
│
├── compression_experiment.py
│   Produces the dictionary compression statistics.
│
├── compare_compressed_queries.py
│   Compares retrieval before and after lossy compression.
│
├── run_spimi_reuters.py
│   Builds the full naive and SPIMI indexes and verifies equality.
│
├── compare_indexing_time.py
│   Compares naive and SPIMI indexing using 10,000 term-DocID pairings.
│
├── validate_reuters_corpus.py
│   Verifies document count, NEWIDs, and extracted documents.
│
├── inspect_reuters_sgm.py
│   Used to inspect different Reuters SGML document types.
│
└── inspect_vocabulary.py
    Used to inspect unusual terms produced by tokenization.
```

## Tokenization and Preprocessing

The base index uses the following main rules:

- Convert terms to lowercase during indexing.
- Discard standalone punctuation.
- Preserve contractions such as `can't`.
- Preserve possessives such as `company's`.
- Split hyphenated terms such as `oil-price`.
- Preserve decimal numbers such as `3.88`.
- Normalize comma-formatted numbers such as `1,850` to `1850`.
- Preserve abbreviations such as `U.S.`.
- Keep standalone numbers in the base index.
- Keep stop words in the base index.
- Do not apply stemming to the base index.

Normal Reuters documents index `TITLE` and `BODY`. Metadata and `DATELINE` are excluded.

Reuters wire-service footer markers are removed before tokenization.

## Key Validation Results

The raw Reuters parser was validated with:

```text
Documents parsed: 21,578
Unique NEWIDs: 21,578
Empty extracted documents: 0
Missing expected NEWIDs: 0
Remaining footer-like documents: 0
```

The final base index contains:

```text
71,682 unique terms
```

The full naive and SPIMI indexes were also compared directly and are identical.

## Subproject IV Timing

The controlled indexing experiment uses exactly:

```text
10,000 term-DocID pairings
```

The same input is supplied to both algorithms.

The experiment is repeated 20 times and the average indexing time is reported.

This timing excludes Reuters parsing and tokenization so that the comparison focuses on the indexing algorithms themselves.

## Notes

The Reuters data is not committed to Git because of its size. It must be placed in `data/reuters21578/` before running the Reuters experiments or demo.

The project parses the original Reuters SGML directly; it does not use the preprocessed Reuters document collection provided by NLTK.