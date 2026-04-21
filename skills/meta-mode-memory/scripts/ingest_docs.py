from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from common import (
    INBOX_DIR,
    INGEST_DIR,
    as_memory_relative,
    as_repo_relative,
    ensure_memory_layout,
    iso_now,
    sha256_file,
    unique_path,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest .md/.txt documents from inbox or explicit paths into .agents/memory/ingest."
    )
    parser.add_argument("paths", nargs="*", help="Optional file or directory paths to ingest.")
    return parser


def gather_candidates(paths: list[str]) -> list[Path]:
    allowed = {".md", ".txt"}
    candidates: list[Path] = []
    if not paths:
        if INBOX_DIR.exists():
            for p in INBOX_DIR.rglob("*"):
                if p.is_file() and p.suffix.lower() in allowed:
                    candidates.append(p)
        return sorted(candidates)
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_file() and p.suffix.lower() in allowed:
            candidates.append(p)
        elif p.is_dir():
            for child in p.rglob("*"):
                if child.is_file() and child.suffix.lower() in allowed:
                    candidates.append(child)
    return sorted(set(candidates))


def ingest_one(src: Path) -> Path:
    target = unique_path(INGEST_DIR / src.name)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    source_repo_rel = as_repo_relative(src)
    copied_repo_rel = as_repo_relative(target)
    copied_memory_rel = as_memory_relative(target)
    meta = {
        "source_path": str(src),
        "source_name": src.name,
        "copied_to": str(target),
        "source_repo_rel": source_repo_rel,
        "copied_repo_rel": copied_repo_rel,
        "copied_memory_rel": copied_memory_rel,
        "ingested_at": iso_now(),
        "size_bytes": target.stat().st_size,
        "sha256": sha256_file(target),
    }
    meta_path = target.with_name(f"{target.name}.meta.json")
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ensure_memory_layout()
    candidates = gather_candidates(args.paths)
    if not candidates:
        print("No .md/.txt files found to ingest.")
        return 0
    ingested: list[Path] = []
    for src in candidates:
        out = ingest_one(src)
        ingested.append(out)
    print(f"Ingested {len(ingested)} file(s):")
    for p in ingested:
        print(f"- {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
