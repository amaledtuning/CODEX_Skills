from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from pathlib import Path
from typing import Iterable

from common import (
    COMPACT_STATE_FIELDS,
    STATE_CHECKPOINTS_DIR,
    STATE_CURRENT_PATH,
    discover_searchable_files,
    read_text,
    safe_terms_from_query,
)


COMPACT_SOURCE_BONUS = 8
COMPACT_TASK_BOOST_TERMS = {
    "task",
    "state",
    "checkpoint",
    "status",
    "facts",
    "decisions",
    "blockers",
    "validation",
    "next",
    "next_steps",
    "sources",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search memory files with deterministic scoring.")
    parser.add_argument("query", nargs="+", help="Query terms")
    parser.add_argument("--limit", type=int, default=8, help="Max results to print")
    return parser


def score_file(path: Path, text: str, terms: list[str], *, source: str = "text") -> tuple[int, str]:
    lower = text.lower()
    file_name = path.name.lower()
    score = 0
    for t in terms:
        score += lower.count(t)
        if t in file_name:
            score += 3
    has_match = score > 0
    is_task_query = any(term in COMPACT_TASK_BOOST_TERMS for term in terms)
    if source == "compact" and (has_match or is_task_query):
        score += COMPACT_SOURCE_BONUS
        if is_task_query:
            score += COMPACT_SOURCE_BONUS
    snippet = best_snippet(text, terms)
    return score, snippet


def best_snippet(text: str, terms: list[str]) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        low = line.lower()
        if any(t in low for t in terms):
            return shorten(line, 180)
    return shorten(lines[0], 180) if lines else "(empty file)"


def shorten(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def compact_state_records() -> list[tuple[Path, str]]:
    records: list[tuple[Path, str]] = []
    if STATE_CURRENT_PATH.exists():
        payload = _read_compact_state(STATE_CURRENT_PATH)
        if payload:
            records.append(
                (
                    STATE_CURRENT_PATH,
                    _format_compact_state_text(payload, source_type="compact-state/current"),
                )
            )

    if STATE_CHECKPOINTS_DIR.exists():
        for path in sorted(STATE_CHECKPOINTS_DIR.glob("*.json")):
            payload = _read_compact_state(path)
            if not payload:
                continue
            records.append(
                (
                    path,
                    _format_compact_state_text(
                        payload,
                        source_type=f"compact-state/checkpoint/{path.stem}",
                    ),
                )
            )
    return records


def _read_compact_state(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(read_text(path))
    except (json.JSONDecodeError, OSError):
        return None
    if isinstance(data, dict):
        return data
    return None


def _compact_to_text(value: Any, limit: int = 200) -> str:
    if isinstance(value, str):
        return _compact_value(str(value), limit)
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray, dict)):
        parts = [_compact_value(str(item), limit=120) for item in value if str(item).strip()]
        return "; ".join(p for p in parts if p)
    return _compact_value(str(value), limit)


def _compact_value(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _format_compact_state_text(payload: dict[str, Any], *, source_type: str) -> str:
    lines = [f"source_type: {source_type}"]
    for field in COMPACT_STATE_FIELDS:
        value = payload.get(field)
        if value is None:
            continue
        rendered = _compact_to_text(value, limit=240)
        if not rendered:
            continue
        lines.append(f"{field}: {rendered}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    terms = safe_terms_from_query(args.query)
    if not terms:
        print("No valid query terms provided.", file=sys.stderr)
        return 2

    hits: list[tuple[int, Path, str]] = []
    for path in discover_searchable_files():
        text = read_text(path)
        score, snippet = score_file(path, text, terms)
        if score > 0:
            hits.append((score, path, snippet))

    for path, text in compact_state_records():
        score, snippet = score_file(path, text, terms, source="compact")
        if score > 0:
            hits.append((score, path, snippet))

    hits.sort(key=lambda item: (-item[0], str(item[1]).lower()))
    if not hits:
        print("No matches found.")
        return 0

    for i, (score, path, snippet) in enumerate(hits[: max(1, args.limit)], start=1):
        print(f"{i}. [score={score}] {path}")
        print(f"   {snippet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
