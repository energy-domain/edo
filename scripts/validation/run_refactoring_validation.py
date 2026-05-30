from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import traceback
import sys

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]

TTL_FILES = [
    ROOT / "core" / "edo.ttl",
    ROOT / "mappings" / "ifc" / "edo-ifc.ttl",
    ROOT / "modules" / "alignments" / "ido" / "edo-ido-alignment.ttl",
]

QUERY_ROOT = ROOT / "queries" / "refactoring"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / f"refactoring-validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"


@dataclass
class QueryResult:
    path: Path
    kind: str
    row_count: int
    ok: bool
    error: str | None = None


def log(message: str = "") -> None:
    # print(message)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(message + "\n")


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def is_informative_query(path: Path) -> bool:
    name = path.name.lower()
    parts = [p.lower() for p in path.parts]

    return (
        "overview" in name
        or "review" in name
        or "list" in name
        or "report" in name
        or "informative" in name
        or "edo-ifc" in parts
    )


def parse_ttl_files() -> Graph:
    graph = Graph()

    log("============================================================")
    log("EDO refactoring validation")
    log("============================================================")
    log(f"Root: {ROOT}")
    log(f"Log:  {LOG_FILE}")
    log("")

    log("Parsing TTL files")
    log("-----------------")

    for ttl_file in TTL_FILES:
        log(f"[TTL] {relative(ttl_file)}")

        if not ttl_file.exists():
            raise FileNotFoundError(f"Missing TTL file: {ttl_file}")

        graph.parse(ttl_file, format="turtle")
        log("      OK")

    log("")
    log(f"Loaded triples: {len(graph)}")
    log("")

    return graph


def run_query(graph: Graph, query_path: Path) -> QueryResult:
    kind = "informative" if is_informative_query(query_path) else "strict"

    try:
        query_text = query_path.read_text(encoding="utf-8")
        rows = list(graph.query(query_text))
        row_count = len(rows)

        ok = kind == "informative" or row_count == 0

        log("------------------------------------------------------------")
        log(f"[QUERY] {relative(query_path)}")
        log(f"Type:   {kind}")
        log(f"Rows:   {row_count}")
        log(f"Status: {'OK' if ok else 'FAILED'}")

        if row_count:
            log("")
            log("Results:")
            for i, row in enumerate(rows, start=1):
                values = [str(value) for value in row]
                log(f"  {i}. " + " | ".join(values))

        log("")

        return QueryResult(
            path=query_path,
            kind=kind,
            row_count=row_count,
            ok=ok,
        )

    except Exception as exc:
        error = "".join(traceback.format_exception_only(type(exc), exc)).strip()

        log("------------------------------------------------------------")
        log(f"[QUERY] {relative(query_path)}")
        log(f"Type:   {kind}")
        log("Status: ERROR")
        log(f"Error:  {error}")
        log("")
        log("Traceback:")
        log(traceback.format_exc())
        log("")

        return QueryResult(
            path=query_path,
            kind=kind,
            row_count=0,
            ok=False,
            error=error,
        )


def run_queries(graph: Graph) -> list[QueryResult]:
    log("Running SPARQL queries")
    log("----------------------")

    if not QUERY_ROOT.exists():
        raise FileNotFoundError(f"Missing query directory: {QUERY_ROOT}")

    query_files = sorted(QUERY_ROOT.rglob("*.rq"))

    if not query_files:
        log("No .rq files found.")
        return []

    results: list[QueryResult] = []

    for query_path in query_files:
        results.append(run_query(graph, query_path))

    return results


def print_summary(results: list[QueryResult]) -> int:
    strict_results = [r for r in results if r.kind == "strict"]
    informative_results = [r for r in results if r.kind == "informative"]

    failed = [r for r in strict_results if not r.ok]
    errors = [r for r in results if r.error is not None]

    log("============================================================")
    log("Summary")
    log("============================================================")
    log(f"Total queries:        {len(results)}")
    log(f"Strict queries:       {len(strict_results)}")
    log(f"Informative queries:  {len(informative_results)}")
    log(f"Strict failures:      {len(failed)}")
    log(f"Query errors:         {len(errors)}")
    log("")

    if failed:
        log("Strict failures:")
        for result in failed:
            log(f"- {relative(result.path)} ({result.row_count} rows)")
        log("")

    if errors:
        log("Query errors:")
        for result in errors:
            log(f"- {relative(result.path)}: {result.error}")
        log("")

    log(f"Log written to: {LOG_FILE}")
    log("")

    if failed or errors:
        log("Validation result: FAILED")
        return 1

    log("Validation result: OK")
    return 0


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    try:
        graph = parse_ttl_files()
        results = run_queries(graph)
        return print_summary(results)

    except Exception:
        log("============================================================")
        log("Fatal error")
        log("============================================================")
        log(traceback.format_exc())
        log(f"Log written to: {LOG_FILE}")
        return 1


if __name__ == "__main__":
    sys.exit(main())