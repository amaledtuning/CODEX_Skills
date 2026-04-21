# Meta Mode Memory Schema

## Root

All data is rooted at:

- default: `<repo>/.agents/memory` (auto-detected from the installed skill path)
- optional override: `META_MODE_MEMORY_ROOT`
- optional repo override (when memory root is defaulted): `META_MODE_MEMORY_REPO_ROOT`

## Directories

- `inbox/`: raw `.md` and `.txt` docs waiting for ingest.
- `daily/`: date-based logs (`YYYY-MM-DD.md`).
- `state/`: compact JSON artifacts (`current.json`, `checkpoints/`).
- `ingest/`: copied ingested docs plus `.meta.json` sidecars.
- `knowledge/`: compiled deterministic knowledge files.
- `knowledge/topics/`: topic pages generated from tags and headings.
- `reports/`: audit output (`latest-audit.md`).

## Daily file format (`daily/YYYY-MM-DD.md`)

```md
# Daily Log YYYY-MM-DD

### [HH:MM:SS] kind: note | Title text
- tags: tag1, tag2
- created_at: YYYY-MM-DDTHH:MM:SS+ZZ:ZZ

Body text (markdown allowed)
```

## Ingest metadata (`ingest/<file>.meta.json`)

```json
{
  "source_path": "absolute path",
  "source_name": "original filename",
  "copied_to": "absolute path in ingest",
  "source_repo_rel": "path relative to repo root (or null)",
  "copied_repo_rel": "path relative to repo root (or null)",
  "copied_memory_rel": "path relative to memory root (or null)",
  "ingested_at": "ISO timestamp",
  "size_bytes": 1234,
  "sha256": "hash"
}
```

## Compiled knowledge outputs

- `knowledge/index.md`: links to log and topic pages.
- `knowledge/log.md`: deterministic summary of daily and ingested sources.
- `knowledge/topics/<topic>.md`: grouped references extracted from:
  - tags in entry metadata or inline `#tag`
  - markdown headings (`#`, `##`, etc.)

## Compact state artifacts

### `state/current.json`

```json
{
  "task_id": "task-uuid",
  "title": "short task title",
  "updated_at": "ISO-8601 timestamp",
  "status": "in_progress | blocked | complete",
  "tags": ["tag1", "tag2"],
  "facts": [
    "compact stable fact 1",
    "compact stable fact 2"
  ],
  "decisions": [
    "decision 1"
  ],
  "blockers": [
    "current blocker"
  ],
  "sources": [
    "daily/YYYY-MM-DD.md",
    "state/current.json"
  ],
  "changed_files": [
    "relative/path/to/file"
  ],
  "validation": [
    "read-only sanity checks only unless explicitly requested"
  ],
  "next_steps": [
    "next action item"
  ]
}
```

### `state/checkpoints/<checkpoint-id>.json`

```json
{
  "checkpoint_id": "YYYYMMDD-HHMMSS-<slug>",
  "created_at": "ISO-8601 timestamp",
  "title": "checkpoint title",
  "task_id": "task-uuid",
  "tags": ["tag1", "tag2"],
  "facts": [...],
  "decisions": [...],
  "blockers": [...],
  "sources": ["daily/YYYY-MM-DD.md"],
  "validation": [...],
  "changed_files": [...],
  "next_steps": [...]
}
```

## Markdown link conventions

- Do not store forbidden content in any state file:
  - raw chat history
  - raw logs
  - long diffs
  - full file contents
  - tokens, credentials, secrets
- Internal links use relative paths from current file.
- No wiki-link syntax required.
- Audit checks standard markdown links: `[label](relative/path.md)`.

## Daily + state checkpoint contract

For each checkpoint, update both:
- one `daily/YYYY-MM-DD.md` entry (human-readable)
- one compact state artifact pair under `state/` (machine-readable)
