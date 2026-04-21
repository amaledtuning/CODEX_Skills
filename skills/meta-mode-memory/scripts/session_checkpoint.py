from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import compile_knowledge
import lint_audit
from common import (
    AUDIT_REPORT_PATH,
    KNOWLEDGE_INDEX_PATH,
    KNOWLEDGE_LOG_PATH,
    append_entry,
    compact_state_checkpoint_path,
    compact_state_current_path,
    ensure_memory_layout,
    iso_now,
    normalize_compact_state,
    now_local,
    slugify,
    write_text,
    today_daily_path,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Append a session checkpoint and optionally compile/lint memory artifacts."
    )
    parser.add_argument("--title", default="Session Checkpoint", help="Entry title")
    parser.add_argument("--kind", default="session", help="Entry kind (default: session)")
    parser.add_argument("--tag", action="append", default=[], help="Tag (repeatable)")
    parser.add_argument("--task-id", help="Optional task identifier")
    parser.add_argument("--status", help="Optional checkpoint status")
    parser.add_argument("--checkpoint-id", help="Optional checkpoint id for compact state file")
    parser.add_argument("--body", help="Inline body text")
    parser.add_argument("--file", help="Read body from file path")
    parser.add_argument("--no-compile", action="store_true", help="Skip compile_knowledge.py")
    parser.add_argument("--no-lint", action="store_true", help="Skip lint_audit.py")
    return parser


def resolve_body(args: argparse.Namespace) -> str:
    if args.body:
        return args.body
    if args.file:
        return Path(args.file).read_text(encoding="utf-8", errors="replace")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise ValueError("No body provided. Use --body, --file, or stdin.")


def _checkpoint_summary(body: str, max_chars: int = 400) -> str:
    compact = " ".join((body or "").split())
    if not compact:
        return ""
    if len(compact) <= max_chars:
        return compact
    return f"{compact[: max_chars - 1]}…"


def _checkpoint_id(args: argparse.Namespace) -> str:
    base = args.task_id or args.title or "session-checkpoint"
    stamp = now_local().strftime("%Y%m%dT%H%M%S%f")
    return f"{stamp}-{slugify(base, fallback='checkpoint')}"


def _compact_payload(args: argparse.Namespace, body: str, checkpoint_id: str) -> dict[str, str | list[str]]:
    summary = _checkpoint_summary(body)
    return normalize_compact_state(
        {
            "task_id": args.task_id,
            "title": args.title,
            "status": args.status,
            "tags": args.tag,
            "facts": [summary] if summary else [],
            "sources": [f"checkpoint:{checkpoint_id}"],
            "updated_at": iso_now(),
        }
    )


def _write_compact_state(payload: dict[str, str | list[str]], checkpoint_id: str) -> None:
    normalized = normalize_compact_state(payload)
    text = json.dumps(normalized, ensure_ascii=False, indent=2) + "\n"
    write_text(compact_state_current_path(), text)
    write_text(compact_state_checkpoint_path(checkpoint_id), text)


def _status_line(label: str, status: str) -> str:
    return f"{label}: {status}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        body = resolve_body(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        ensure_memory_layout()
        appended_path = append_entry(
            path=today_daily_path(),
            kind=args.kind,
            title=args.title,
            tags=args.tag,
            body=body,
        )

        checkpoint_id = (
            slugify(args.checkpoint_id, fallback="checkpoint")
            if args.checkpoint_id
            else _checkpoint_id(args)
        )
        compact_payload = _compact_payload(args, body, checkpoint_id)
        _write_compact_state(compact_payload, checkpoint_id)
    except Exception as exc:  # pragma: no cover - defensive error boundary for CLI
        print(f"Failed to append checkpoint: {exc}", file=sys.stderr)
        return 1

    compile_status = "skipped (--no-compile)"
    lint_status = "skipped (--no-lint)"
    failed = False

    if not args.no_compile:
        rc = compile_knowledge.main([])
        if rc == 0:
            compile_status = "ok"
        else:
            compile_status = f"failed (exit={rc})"
            failed = True
    if not args.no_lint:
        if not args.no_compile and failed:
            lint_status = "skipped (compile failed)"
        else:
            rc = lint_audit.main([])
            if rc == 0:
                lint_status = "ok"
            else:
                lint_status = f"failed (exit={rc})"
                failed = True

    print(f"Appended: {appended_path}")
    print(_status_line("Compile", compile_status))
    print(f"Knowledge index: {KNOWLEDGE_INDEX_PATH}")
    print(f"Knowledge log: {KNOWLEDGE_LOG_PATH}")
    print(_status_line("Lint", lint_status))
    print(f"Audit report: {AUDIT_REPORT_PATH}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
