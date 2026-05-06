from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import append_entry, ensure_memory_layout, today_daily_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append a structured entry to today's daily log.")
    parser.add_argument("--title", default="Session Entry", help="Entry title")
    parser.add_argument("--kind", default="session", help="Entry kind (session/reflection/decision/etc.)")
    parser.add_argument("--tag", action="append", default=[], help="Tag (repeatable)")
    parser.add_argument("--body", help="Inline body text")
    parser.add_argument("--file", help="Read body from file path")
    return parser


def resolve_body(args: argparse.Namespace) -> str:
    if args.body:
        return args.body
    if args.file:
        return Path(args.file).read_text(encoding="utf-8", errors="replace")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise ValueError("No body provided. Use --body, --file, or stdin.")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        body = resolve_body(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    ensure_memory_layout()
    out_path = append_entry(
        path=today_daily_path(),
        kind=args.kind,
        title=args.title,
        tags=args.tag,
        body=body,
    )
    print(f"Appended daily entry: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

