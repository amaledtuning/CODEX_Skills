from __future__ import annotations

import hashlib
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ENV_REPO_ROOT = "META_MODE_MEMORY_REPO_ROOT"
ENV_MEMORY_ROOT = "META_MODE_MEMORY_ROOT"


def _norm_path(path_value: str) -> Path:
    return Path(path_value).expanduser().resolve(strict=False)


def _looks_like_repo_root(path: Path) -> bool:
    skill_dir = path / ".agents" / "skills" / "meta-mode-memory"
    return (skill_dir / "scripts" / "common.py").exists()


def _detect_repo_root() -> Path:
    search_bases = [Path(__file__).resolve(), Path.cwd().resolve()]
    for base in search_bases:
        for candidate in [base, *base.parents]:
            if _looks_like_repo_root(candidate):
                return candidate
    return Path.cwd().resolve()


def _resolve_roots() -> tuple[Path, Path]:
    repo_override = os.environ.get(ENV_REPO_ROOT, "").strip()
    memory_override = os.environ.get(ENV_MEMORY_ROOT, "").strip()

    repo_root = _norm_path(repo_override) if repo_override else _detect_repo_root()

    if memory_override:
        memory_root = _norm_path(memory_override)
        return repo_root, memory_root

    return repo_root, repo_root / ".codex-memory"


REPO_ROOT, MEMORY_ROOT = _resolve_roots()
INBOX_DIR = MEMORY_ROOT / "inbox"
DAILY_DIR = MEMORY_ROOT / "daily"
INGEST_DIR = MEMORY_ROOT / "ingest"
KNOWLEDGE_DIR = MEMORY_ROOT / "knowledge"
TOPICS_DIR = KNOWLEDGE_DIR / "topics"
REPORTS_DIR = MEMORY_ROOT / "reports"
STATE_DIR = MEMORY_ROOT / "state"
STATE_CURRENT_PATH = STATE_DIR / "current.json"
STATE_CHECKPOINTS_DIR = STATE_DIR / "checkpoints"
AUDIT_REPORT_PATH = REPORTS_DIR / "latest-audit.md"
KNOWLEDGE_INDEX_PATH = KNOWLEDGE_DIR / "index.md"
KNOWLEDGE_LOG_PATH = KNOWLEDGE_DIR / "log.md"


def now_local() -> datetime:
    return datetime.now().astimezone()


def iso_now() -> str:
    return now_local().isoformat(timespec="seconds")


def today_str() -> str:
    return now_local().date().isoformat()


def today_daily_path() -> Path:
    return DAILY_DIR / f"{today_str()}.md"


def ensure_memory_layout() -> None:
    for path in [
        MEMORY_ROOT,
        INBOX_DIR,
        DAILY_DIR,
        INGEST_DIR,
        KNOWLEDGE_DIR,
        TOPICS_DIR,
        REPORTS_DIR,
        STATE_DIR,
        STATE_CHECKPOINTS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def normalize_ws(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(value: str, fallback: str = "item") -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value).strip("-")
    return value or fallback


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    i = 1
    while True:
        candidate = path.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_link(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, from_file.parent)).as_posix()


def as_repo_relative(path: Path) -> str | None:
    try:
        return path.resolve(strict=False).relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return None


def as_memory_relative(path: Path) -> str | None:
    try:
        return path.resolve(strict=False).relative_to(MEMORY_ROOT).as_posix()
    except ValueError:
        return None


COMPACT_STATE_FIELDS = (
    "task_id",
    "title",
    "updated_at",
    "status",
    "facts",
    "decisions",
    "do_not_reask_decisions",
    "blockers",
    "changed_files",
    "validation",
    "next_steps",
    "tags",
    "sources",
)
COMPACT_STATE_DEFAULT_STATUS = "in_progress"
COMPACT_STATE_LIST_LIMITS = {
    "facts": 20,
    "decisions": 20,
    "do_not_reask_decisions": 20,
    "blockers": 20,
    "changed_files": 30,
    "validation": 20,
    "next_steps": 20,
    "tags": 20,
    "sources": 20,
}
COMPACT_STATE_ITEM_LIMIT = 1800
COMPACT_STATE_TEXT_LIMIT = 400
COMPACT_STATE_PATH_LEN_LIMIT = 240


def extract_hashtags(text: str) -> list[str]:
    tags = re.findall(r"(?<!\w)#([A-Za-z0-9][\w-]{0,63})", text or "")
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


def extract_headings(text: str) -> list[str]:
    out: list[str] = []
    for line in (text or "").splitlines():
        m = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if m:
            heading = m.group(1).strip()
            if heading:
                out.append(heading)
    return out


def compact_state_current_path() -> Path:
    return STATE_CURRENT_PATH


def compact_state_checkpoint_path(checkpoint_id: str) -> Path:
    return STATE_CHECKPOINTS_DIR / f"{slugify(checkpoint_id)}.json"


def _compact_trim_text(value: Any, max_len: int = COMPACT_STATE_TEXT_LIMIT) -> str:
    text = str(value or "").strip()
    if len(text) <= max_len:
        return text
    if max_len <= 1:
        return "…"
    return f"{text[: max_len - 1]}\u2026"


def _compact_to_list(
    value: Any,
    *,
    max_items: int,
    max_len: int = COMPACT_STATE_TEXT_LIMIT,
    keep_order: bool = True,
) -> list[str]:
    items: list[str] = []
    if isinstance(value, Mapping):
        items = [f"{k}: {v}" for k, v in value.items()]
    elif isinstance(value, (list, tuple, set)):
        items = [str(v) for v in value]
    elif isinstance(value, str):
        text = value.strip()
        if text:
            items = [text]
    elif value is not None:
        items = [str(value)]

    source = items if keep_order else sorted(set(items))
    normalized: list[str] = []
    seen: set[str] = set()
    for item in source:
        item_text = _compact_trim_text(item.replace("\n", " ").strip(), max_len=max_len)
        if not item_text:
            continue
        item_text = item_text[:COMPACT_STATE_ITEM_LIMIT]
        if not item_text or item_text in seen:
            continue
        seen.add(item_text)
        normalized.append(item_text)
        if len(normalized) >= max_items:
            break
    return normalized


def normalize_compact_state(payload: Mapping[str, Any] | None) -> dict[str, str | list[str]]:
    data = payload or {}
    status = _compact_trim_text(data.get("status", COMPACT_STATE_DEFAULT_STATUS), max_len=COMPACT_STATE_TEXT_LIMIT)
    status = status.lower().strip() or COMPACT_STATE_DEFAULT_STATUS

    return {
        "task_id": _compact_trim_text(data.get("task_id"), max_len=COMPACT_STATE_TEXT_LIMIT),
        "title": _compact_trim_text(data.get("title"), max_len=COMPACT_STATE_TEXT_LIMIT),
        "updated_at": _compact_trim_text(data.get("updated_at"), max_len=COMPACT_STATE_TEXT_LIMIT),
        "status": status,
        "facts": _compact_to_list(data.get("facts"), max_items=COMPACT_STATE_LIST_LIMITS["facts"]),
        "decisions": _compact_to_list(
            data.get("decisions"), max_items=COMPACT_STATE_LIST_LIMITS["decisions"]
        ),
        "do_not_reask_decisions": _compact_to_list(
            data.get("do_not_reask_decisions"),
            max_items=COMPACT_STATE_LIST_LIMITS["do_not_reask_decisions"],
        ),
        "blockers": _compact_to_list(data.get("blockers"), max_items=COMPACT_STATE_LIST_LIMITS["blockers"]),
        "changed_files": _compact_to_list(
            data.get("changed_files"),
            max_items=COMPACT_STATE_LIST_LIMITS["changed_files"],
            max_len=COMPACT_STATE_PATH_LEN_LIMIT,
            keep_order=False,
        ),
        "validation": _compact_to_list(
            data.get("validation"), max_items=COMPACT_STATE_LIST_LIMITS["validation"]
        ),
        "next_steps": _compact_to_list(
            data.get("next_steps"), max_items=COMPACT_STATE_LIST_LIMITS["next_steps"]
        ),
        "tags": _compact_to_list(
            data.get("tags"), max_items=COMPACT_STATE_LIST_LIMITS["tags"], max_len=96, keep_order=False
        ),
        "sources": _compact_to_list(
            data.get("sources"), max_items=COMPACT_STATE_LIST_LIMITS["sources"]
        ),
    }


WORD_RE = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text or "")]


def split_csv_tags(tag_text: str) -> list[str]:
    if not tag_text:
        return []
    return [p.strip().lower() for p in tag_text.split(",") if p.strip()]


def format_entry(kind: str, title: str, tags: Iterable[str], body: str) -> str:
    ts = now_local().strftime("%H:%M:%S")
    clean_tags = [t.strip() for t in tags if t and t.strip()]
    clean_body = normalize_ws(body)
    lines = [
        f"### [{ts}] kind: {kind} | {title}",
        f"- tags: {', '.join(clean_tags) if clean_tags else '(none)'}",
        f"- created_at: {iso_now()}",
        "",
        clean_body or "(empty)",
        "",
    ]
    return "\n".join(lines)


def ensure_daily_header(path: Path) -> None:
    if path.exists():
        return
    date_part = path.stem
    path.write_text(f"# Daily Log {date_part}\n\n", encoding="utf-8")


def append_entry(path: Path, kind: str, title: str, tags: Iterable[str], body: str) -> Path:
    ensure_memory_layout()
    ensure_daily_header(path)
    entry = format_entry(kind=kind, title=title, tags=tags, body=body)
    with path.open("a", encoding="utf-8") as f:
        if path.stat().st_size > 0 and not _ends_with_blank_line(path):
            f.write("\n")
        f.write(entry)
    return path


def _ends_with_blank_line(path: Path) -> bool:
    content = read_text(path)
    return content.endswith("\n\n")


def discover_searchable_files() -> list[Path]:
    files: list[Path] = []
    for base, patterns in [
        (DAILY_DIR, ("*.md",)),
        (INGEST_DIR, ("*.md", "*.txt")),
        (KNOWLEDGE_DIR, ("*.md",)),
    ]:
        if not base.exists():
            continue
        for pattern in patterns:
            files.extend(base.rglob(pattern))
    # Exclude ingest metadata sidecars from search corpus.
    files = [p for p in files if not p.name.endswith(".meta.json")]
    return sorted(set(files))


ENTRY_HEADER_RE = re.compile(r"^### \[(?P<time>[^\]]+)\] kind: (?P<kind>[^|]+)\| (?P<title>.+)$", re.MULTILINE)
TAGS_LINE_RE = re.compile(r"^- tags:\s*(?P<tags>.+?)\s*$", re.MULTILINE)
CREATED_AT_LINE_RE = re.compile(r"^- created_at:\s*(?P<created_at>.+?)\s*$", re.MULTILINE)
def parse_daily_entries(path: Path) -> list[dict[str, str | list[str]]]:
    content = read_text(path)
    matches = list(ENTRY_HEADER_RE.finditer(content))
    entries: list[dict[str, str | list[str]]] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        block = content[start:end].strip()
        tags_match = TAGS_LINE_RE.search(block)
        created_at_match = CREATED_AT_LINE_RE.search(block)
        body = block
        if created_at_match:
            body = block[created_at_match.end() :].strip()
        elif tags_match:
            body = block[tags_match.end() :].strip()
        tags = split_csv_tags(tags_match.group("tags")) if tags_match else []
        body = body.strip() if body else ""
        entries.append(
            {
                "time": match.group("time").strip(),
                "kind": match.group("kind").strip(),
                "title": match.group("title").strip(),
                "tags": tags,
                "created_at": created_at_match.group("created_at").strip() if created_at_match else "",
                "body": body,
            }
        )
    return entries


def safe_terms_from_query(parts: Sequence[str]) -> list[str]:
    terms: list[str] = []
    for part in parts:
        terms.extend(tokenize(part))
    deduped: list[str] = []
    seen: set[str] = set()
    for t in terms:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped
