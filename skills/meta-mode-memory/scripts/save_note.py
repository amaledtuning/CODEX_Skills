from __future__ import annotations

import argparse
import sys

from common import append_entry, ensure_memory_layout, today_daily_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quick-save a note entry into today's daily log.")
    parser.add_argument("text", help="Note body text")
    parser.add_argument("--title", default="Quick Note", help="Entry title")
    parser.add_argument("--tag", action="append", default=[], help="Tag (repeatable)")
    parser.add_argument("--kind", default="note", help="Entry kind (default: note)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ensure_memory_layout()
    out_path = append_entry(
        path=today_daily_path(),
        kind=args.kind,
        title=args.title,
        tags=args.tag,
        body=args.text,
    )
    print(f"Saved note to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
