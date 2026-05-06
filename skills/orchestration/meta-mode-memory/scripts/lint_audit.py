from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    AUDIT_REPORT_PATH,
    DAILY_DIR,
    INBOX_DIR,
    INGEST_DIR,
    KNOWLEDGE_DIR,
    KNOWLEDGE_INDEX_PATH,
    KNOWLEDGE_LOG_PATH,
    MEMORY_ROOT,
    REPORTS_DIR,
    TOPICS_DIR,
    ensure_memory_layout,
    parse_daily_entries,
    read_text,
    write_text,
)


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_MARKERS = ("ghp_", "github_pat_", "AIza", "sk-", "MRKTNG")
OVERSIZE_BYTES = 200_000
COMPACT_OBJECT_FIELD_LIMIT = 64
COMPACT_LIST_ITEM_LIMIT = 256


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Lint and audit Meta Mode memory files.")


def _scan_compact_state_file(state_file: Path, errors: list[str], warnings: list[str]) -> None:
    try:
        content = state_file.read_text(encoding="utf-8")
    except OSError as e:
        errors.append(f"Cannot read compact state file `{state_file}`: {e}")
        return

    try:
        payload = json.loads(content)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in `{state_file}`: {e}")
        return

    if not isinstance(payload, dict):
        errors.append(f"Compact state root is not an object in `{state_file}`")
        return

    if len(payload) > COMPACT_OBJECT_FIELD_LIMIT:
        warnings.append(
            f"Large compact object in `{state_file}`: {len(payload)} top-level fields "
            f"(compact expectation is <= {COMPACT_OBJECT_FIELD_LIMIT})"
        )

    def _walk(value: object, pointer: str) -> None:
        if isinstance(value, dict):
            if len(value) > COMPACT_OBJECT_FIELD_LIMIT:
                warnings.append(
                    f"Large dictionary in `{state_file}` at `{pointer}`: {len(value)} fields"
                )
            for key, nested in value.items():
                if len(str(key)) > 120:
                    warnings.append(
                        f"Unusually long key in `{state_file}` at `{pointer}.{key}` ({len(str(key))} chars)"
                    )
                _walk(nested, f"{pointer}.{key}")
            return

        if isinstance(value, list):
            if len(value) > COMPACT_LIST_ITEM_LIMIT:
                warnings.append(
                    f"Large list in `{state_file}` at `{pointer}`: {len(value)} items"
                )
            for i, nested in enumerate(value):
                _walk(nested, f"{pointer}[{i}]")
            return

        if isinstance(value, str):
            if len(value.encode("utf-8")) > OVERSIZE_BYTES:
                errors.append(
                    f"Oversized string value in `{state_file}` at `{pointer}` ({len(value.encode('utf-8'))} bytes)"
                )

    _walk(payload, "$")


def _scan_secret_markers(memory_root: Path, warnings: list[str]) -> None:
    for file_path in sorted(memory_root.rglob("*")):
        if not file_path.is_file():
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for marker in SECRET_MARKERS:
            count = content.count(marker)
            if count:
                warnings.append(
                    f"Potential secret marker `{marker}` in `{file_path}`: {count} hit(s)"
                )


def _scan_markdown_links(md_file: Path) -> list[tuple[Path, str]]:
    issues: list[tuple[Path, str]] = []
    content = read_text(md_file)
    for target in MARKDOWN_LINK_RE.findall(content):
        target = target.strip()
        if not target:
            continue
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (md_file.parent / target).resolve()
        if not resolved.exists():
            issues.append((md_file, target))
    return issues


def main(argv: list[str] | None = None) -> int:
    _ = build_parser().parse_args(argv)
    ensure_memory_layout()

    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    expected_dirs = [MEMORY_ROOT, INBOX_DIR, DAILY_DIR, INGEST_DIR, KNOWLEDGE_DIR, TOPICS_DIR, REPORTS_DIR]
    for d in expected_dirs:
        if not d.exists():
            errors.append(f"Missing directory: `{d}`")

    for expected_file in [KNOWLEDGE_INDEX_PATH, KNOWLEDGE_LOG_PATH]:
        if not expected_file.exists():
            warnings.append(f"Missing compiled file: `{expected_file}` (run compile_knowledge.py)")

    md_files = []
    for base in [DAILY_DIR, KNOWLEDGE_DIR, TOPICS_DIR]:
        if base.exists():
            md_files.extend(base.rglob("*.md"))
    link_issues: list[str] = []
    for md in sorted(set(md_files)):
        for source, target in _scan_markdown_links(md):
            link_issues.append(f"Broken link in `{source}` -> `{target}`")
    warnings.extend(link_issues)

    if DAILY_DIR.exists():
        for daily in sorted(DAILY_DIR.glob("*.md")):
            entries = parse_daily_entries(daily)
            for idx, entry in enumerate(entries, start=1):
                body = str(entry.get("body", "")).strip()
                if not body or body == "(empty)":
                    warnings.append(f"Empty daily entry in `{daily}` at entry #{idx}")

    if KNOWLEDGE_DIR.exists():
        for p in KNOWLEDGE_DIR.rglob("*.md"):
            size = p.stat().st_size
            if size > OVERSIZE_BYTES:
                warnings.append(f"Oversized knowledge page `{p}` ({size} bytes)")

    state_root = MEMORY_ROOT / "state"
    if state_root.exists():
        current_state = state_root / "current.json"
        if current_state.exists():
            _scan_compact_state_file(current_state, errors, warnings)

        checkpoint_dir = state_root / "checkpoints"
        if checkpoint_dir.exists():
            for checkpoint in sorted(checkpoint_dir.glob("*.json")):
                _scan_compact_state_file(checkpoint, errors, warnings)

    if MEMORY_ROOT.exists():
        _scan_secret_markers(MEMORY_ROOT, warnings)

    if not errors and not warnings:
        infos.append("No structural issues detected.")

    report_lines = [
        "# Memory Audit Report",
        "",
        "## Summary",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        f"- Info: {len(infos)}",
        "",
    ]
    if errors:
        report_lines.append("## Errors")
        for item in errors:
            report_lines.append(f"- {item}")
        report_lines.append("")
    if warnings:
        report_lines.append("## Warnings")
        for item in warnings:
            report_lines.append(f"- {item}")
        report_lines.append("")
    if infos:
        report_lines.append("## Info")
        for item in infos:
            report_lines.append(f"- {item}")
        report_lines.append("")

    write_text(AUDIT_REPORT_PATH, "\n".join(report_lines))
    print(f"Audit complete: errors={len(errors)} warnings={len(warnings)} info={len(infos)}")
    print(f"Report: {AUDIT_REPORT_PATH}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
