from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    DAILY_DIR,
    INGEST_DIR,
    KNOWLEDGE_DIR,
    KNOWLEDGE_INDEX_PATH,
    KNOWLEDGE_LOG_PATH,
    COMPACT_STATE_FIELDS,
    STATE_CHECKPOINTS_DIR,
    STATE_CURRENT_PATH,
    normalize_compact_state,
    TOPICS_DIR,
    ensure_memory_layout,
    extract_hashtags,
    extract_headings,
    parse_daily_entries,
    read_text,
    rel_link,
    slugify,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Compile deterministic knowledge pages from daily and ingested sources.")


def _collect_daily_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    if not DAILY_DIR.exists():
        return records
    for path in sorted(DAILY_DIR.glob("*.md")):
        entries = parse_daily_entries(path)
        for e in entries:
            title = str(e.get("title", "")).strip() or path.stem
            body = str(e.get("body", "")).strip()
            tags = [str(t).lower() for t in (e.get("tags") or [])]
            tags.extend(extract_hashtags(f"{title}\n{body}"))
            tags = sorted(set(tags))
            headings = extract_headings(body)
            records.append(
                {
                    "source_path": path,
                    "source_kind": "daily",
                    "entry_kind": str(e.get("kind", "")).strip() or "note",
                    "title": title,
                    "tags": tags,
                    "headings": headings,
                    "body": body,
                }
            )
    return records


def _collect_ingest_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    if not INGEST_DIR.exists():
        return records
    for path in sorted(INGEST_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        if path.name.endswith(".meta.json"):
            continue
        text = read_text(path)
        headings = extract_headings(text)
        title = headings[0] if headings else path.stem
        tags = extract_hashtags(text)
        tags.extend([slugify(h, fallback="topic") for h in headings[:8]])
        tags = [t for t in tags if t and t != "topic"]
        tags = sorted(set(tags))
        records.append(
            {
                "source_path": path,
                "source_kind": "ingest",
                "entry_kind": "doc",
                "title": title,
                "tags": tags,
                "headings": headings,
                "body": text,
            }
        )
    return records


def _load_compact_state(path: Path) -> dict[str, object] | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    normalized = normalize_compact_state(data)
    return {str(k): v for k, v in normalized.items() if k in COMPACT_STATE_FIELDS}


def _build_compact_state_snippet(state: dict[str, object]) -> str:
    lines: list[str] = []
    for key in ("task_id", "title", "status", "updated_at"):
        value = str(state.get(key, "")).strip()
        if value:
            lines.append(f"{key}: {value}")

    for key in ("facts", "decisions", "blockers", "validation", "next_steps", "sources", "changed_files"):
        value = state.get(key)
        if not isinstance(value, list):
            continue
        for item in value[:2]:
            text = str(item).strip()
            if text:
                label = key[:-1] if key.endswith("s") else key
                lines.append(f"{label}: {text}")

    return "\n".join(lines) if lines else "(no compact details)"


def _compact_state_tags(state: dict[str, object]) -> list[str]:
    tags: list[str] = []
    for key in ("status", "task_id"):
        value = str(state.get(key, "")).strip().lower()
        if value and value != "in_progress":
            tags.append(value)

    raw_tags = state.get("tags")
    if isinstance(raw_tags, list):
        for raw_tag in raw_tags[:6]:
            tag = str(raw_tag).strip().lower()
            if tag:
                tags.append(tag)

    deduped: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        if tag in seen:
            continue
        seen.add(tag)
        deduped.append(tag)
    return sorted(deduped)


def _collect_compact_state_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    state_paths: list[tuple[str, Path]] = []

    if STATE_CURRENT_PATH.exists():
        state_paths.append(("compact_state_current", STATE_CURRENT_PATH))
    if STATE_CHECKPOINTS_DIR.exists():
        state_paths.extend((("compact_state_checkpoint", p) for p in sorted(STATE_CHECKPOINTS_DIR.glob("*.json"))))

    for source_kind, path in state_paths:
        state = _load_compact_state(path)
        if not state:
            continue
        snippet = _build_compact_state_snippet(state)
        tags = _compact_state_tags(state)
        tags.append(f"source:{path.name}")
        title = str(state.get("title", "")).strip() or path.stem
        headings = [str(v).strip() for v in (state.get("task_id"), state.get("status"), state.get("title")) if str(v).strip()]

        records.append(
            {
                "source_path": path,
                "source_kind": source_kind,
                "entry_kind": "compact_state",
                "title": title,
                "tags": tags,
                "headings": headings,
                "body": snippet,
            }
        )

    return records


def _topic_candidates(record: dict[str, object]) -> list[str]:
    topics: list[str] = []
    for tag in record.get("tags", []):
        tag_s = str(tag).strip().lower()
        if tag_s and tag_s != "(none)":
            topics.append(tag_s)
    for heading in record.get("headings", []):
        h = str(heading).strip()
        if not h:
            continue
        h = re.sub(r"`+", "", h)
        if len(h) > 64:
            h = h[:64].rstrip()
        topics.append(slugify(h, fallback="topic"))
    deduped: list[str] = []
    seen: set[str] = set()
    for t in topics:
        if t not in seen and t:
            seen.add(t)
            deduped.append(t)
    return deduped[:12]


def _build_topic_pages(records: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for record in records:
        for topic in _topic_candidates(record):
            grouped.setdefault(topic, []).append(record)
    for topic in grouped:
        grouped[topic] = sorted(
            grouped[topic],
            key=lambda r: (str(r.get("source_kind", "")), str(Path(str(r.get("source_path"))))),
        )
    for topic, topic_records in sorted(grouped.items(), key=lambda kv: kv[0]):
        topic_path = TOPICS_DIR / f"{slugify(topic, fallback='topic')}.md"
        lines = [f"# Topic: {topic}", ""]
        for record in topic_records:
            source_path = Path(str(record["source_path"]))
            source_link = rel_link(topic_path, source_path)
            title = str(record.get("title", source_path.stem))
            entry_kind = str(record.get("entry_kind", "item"))
            lines.append(f"- [{title}]({source_link}) (`{entry_kind}`)")
        lines.append("")
        write_text(topic_path, "\n".join(lines))
    return grouped


def _clean_old_topic_pages(valid_topics: set[str]) -> None:
    if not TOPICS_DIR.exists():
        return
    for path in TOPICS_DIR.glob("*.md"):
        if path.stem not in valid_topics:
            path.unlink()


def _build_log(records: list[dict[str, object]]) -> None:
    lines = ["# Knowledge Log", ""]
    daily_records = [r for r in records if r.get("source_kind") == "daily"]
    ingest_records = [r for r in records if r.get("source_kind") == "ingest"]
    state_records = [r for r in records if str(r.get("source_kind", "")).startswith("compact_state")]

    lines.append("## Daily Sources")
    if not daily_records:
        lines.append("- (none)")
    else:
        for r in daily_records:
            source_path = Path(str(r["source_path"]))
            link = rel_link(KNOWLEDGE_LOG_PATH, source_path)
            title = str(r.get("title", source_path.stem))
            kind = str(r.get("entry_kind", "note"))
            tags = ", ".join(str(t) for t in (r.get("tags") or [])[:6]) or "(none)"
            lines.append(f"- [{title}]({link}) (`{kind}`) tags: {tags}")
    lines.append("")

    lines.append("## Ingested Sources")
    if not ingest_records:
        lines.append("- (none)")
    else:
        for r in ingest_records:
            source_path = Path(str(r["source_path"]))
            link = rel_link(KNOWLEDGE_LOG_PATH, source_path)
            title = str(r.get("title", source_path.stem))
            tags = ", ".join(str(t) for t in (r.get("tags") or [])[:6]) or "(none)"
            lines.append(f"- [{title}]({link}) tags: {tags}")
    lines.append("")

    lines.append("## Compact State Sources")
    if not state_records:
        lines.append("- (none)")
    else:
        for r in state_records:
            source_path = Path(str(r["source_path"]))
            link = rel_link(KNOWLEDGE_LOG_PATH, source_path)
            title = str(r.get("title", source_path.stem))
            kind = str(r.get("source_kind", "compact_state"))
            tags = ", ".join(str(t) for t in (r.get("tags") or [])[:6]) or "(none)"
            lines.append(f"- [{title}]({link}) (`{kind}`) tags: {tags}")
    lines.append("")

    write_text(KNOWLEDGE_LOG_PATH, "\n".join(lines))


def _build_index(topic_map: dict[str, list[dict[str, object]]], records: list[dict[str, object]]) -> None:
    lines = ["# Memory Knowledge Index", ""]
    lines.append("- [Knowledge Log](log.md)")
    lines.append("")
    lines.append("## Topics")
    if not topic_map:
        lines.append("- (none)")
    else:
        for topic, refs in sorted(topic_map.items(), key=lambda kv: kv[0]):
            slug = slugify(topic, fallback="topic")
            lines.append(f"- [{topic}](topics/{slug}.md) ({len(refs)} refs)")
    lines.append("")
    lines.append("## Stats")
    lines.append(f"- Daily entries: {len([r for r in records if r.get('source_kind') == 'daily'])}")
    lines.append(f"- Ingest docs: {len([r for r in records if r.get('source_kind') == 'ingest'])}")
    lines.append(
        f"- Compact state records: {len([r for r in records if str(r.get('source_kind', '')).startswith('compact_state')])}"
    )
    lines.append("")
    write_text(KNOWLEDGE_INDEX_PATH, "\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    _ = build_parser().parse_args(argv)
    ensure_memory_layout()
    records = (
        _collect_daily_records()
        + _collect_ingest_records()
        + _collect_compact_state_records()
    )
    topic_map = _build_topic_pages(records)
    _clean_old_topic_pages({slugify(t, fallback="topic") for t in topic_map.keys()})
    _build_log(records)
    _build_index(topic_map, records)
    print(f"Compiled knowledge: {KNOWLEDGE_INDEX_PATH}")
    print(f"Compiled log: {KNOWLEDGE_LOG_PATH}")
    print(f"Topics generated: {len(topic_map)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
