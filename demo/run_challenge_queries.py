from pathlib import Path
from time import perf_counter

from ir_project.corpus import iter_documents
from ir_project.naive_indexer import build_naive_index
from ir_project.query_processor import process_query
from ir_project.spimi_indexer import build_spimi_index


DEMO_ROOT = Path(__file__).resolve().parent

QUERY_FILE = DEMO_ROOT / "challenge_queries.txt"

OUTPUT_DIR = DEMO_ROOT / "challenge_output"
OUTPUT_FILE = OUTPUT_DIR / "challenge_results.txt"


def _load_queries(path: Path) -> list[str]:
    """Load non-empty challenge queries, one query per line."""

    if not path.exists():
        raise FileNotFoundError(f"Challenge query file not found: {path}")

    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def timed_query(
    index: dict[str, list[int]],
    query: str,
) -> tuple[list[int], float]:
    """Run one query and return its results and execution time."""

    start = perf_counter()
    results = process_query(index, query)
    elapsed = perf_counter() - start

    return results, elapsed


def main():
    queries = _load_queries(QUERY_FILE)

    if not queries:
        raise ValueError("No challenge queries were found.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    def output(text: str="") -> None:
        print(text)
        lines.append(text)

    output("=" * 70)
    output("COMP 479 - CHallenge Query Results")
    output("=" * 70)

    output()
    output(f"Queries loaded: {len(queries)}")

    # Build Naive Index
    output()
    output("Building Naive Index...")

    start = perf_counter()
    naive_index = build_naive_index(iter_documents())
    naive_build_time = perf_counter() - start

    output(f"Naive build time: {naive_build_time:.6f} seconds")
    output(f"Naive unique terms: {len(naive_index):,}")

    # Build SPIMI Index
    output()
    output("Building SPIMI Index...")

    start = perf_counter()
    spimi_index = build_naive_index(iter_documents())
    spimi_build_time = perf_counter() - start

    output(f"SPIMI build time: {spimi_build_time:.6f} seconds")
    output(f"SPIMI unique terms: {len(spimi_index):,}")

    output()
    output(f"Indexes match: {naive_index == spimi_index}")

    # Challenge Queries
    naive_total = 0.0
    spimi_total = 0.0

    for number, query in enumerate(queries, start=1):
        naive_results, naive_time = timed_query(naive_index, query)

        spimi_results, spimi_time = timed_query(spimi_index, query)

        naive_total += naive_time
        spimi_total += spimi_time

        output()
        output("=" * 70)
        output(f"Challenge Query {number}: {query}")
        output("=" * 70)

        output()
        output("Naive Indexer")
        output("-" * 70)
        output(f"Documents found: {len(naive_results):,}")
        output(f"DocIDs: {naive_results}")
        output(f"Query time: {naive_time:.9f} seconds")

        output()
        output("SPIMI Indexer")
        output("-" * 70)
        output(f"Dcoument found: {len(spimi_results):,}")
        output(f"DocIDs: {spimi_results}")
        output(f"Query time: {spimi_time:.9f} seconds")

        output()
        output(f"Result match: {naive_results == spimi_results}")

    # Timing Summary
    output()
    output("=" * 70)
    output("Timing Summary")
    output("=" * 70)

    output(f"Naive build time: {naive_build_time:.6f} seconds")
    output(f"SPIMI build time: {spimi_build_time:.6f} seconds")

    output()
    output(f"Naive total challenge query time: {naive_total:.9f} seconds")
    output(f"SPIMI total challenge query time: {spimi_total:.9f} seconds")

    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print()
    print(f"Results saved to: {OUTPUT_FILE}")