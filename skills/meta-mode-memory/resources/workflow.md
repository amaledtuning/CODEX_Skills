# Meta Mode Memory Workflow

Canonical Codex usage for this memory MVP:

1. Before work: query memory via a read-only memory scout/subagent using `query_memory.py`.
2. During work: save compact durable facts via `save_note.py` with concise source-oriented tags.
3. After meaningful work: capture one compact markdown checkpoint entry and run `session_checkpoint.py` with stable facts, decisions, blockers, validation, changed files, and next steps.
4. `session_checkpoint.py` must synchronize compact state:
   - update `.agents/memory/state/current.json`
   - append `.agents/memory/state/checkpoints/<id>.json`
   - keep a matching markdown entry in `daily/`.
5. Under the active policy stack for this session: keep memory inspection in the allowed worker/scout execution lane instead of bypassing role boundaries.
6. Keep entries concise, attributable, and useful for later retrieval.
7. Avoid raw logs, long diffs, full file contents, and any secrets/tokens.

Recommended end-of-session command:

```powershell
python .agents/skills/meta-mode-memory/scripts/session_checkpoint.py --title "Session checkpoint" --tag feature --body "- Summary\n- Stable facts\n- Decisions\n- Blockers\n- Validation\n- Changed files\n- Next steps"
```

Checkpoint flow pattern:

1. `append_daily_log.py` writes:
   - markdown in `daily/YYYY-MM-DD.md`
   - machine-usable facts (short bullets)
2. `session_checkpoint.py` writes:
   - compact JSON updates under `state/current.json`
   - immutable snapshot under `state/checkpoints/<checkpoint-id>.json`
3. Optional follow-up:
   - ingest docs and compile as needed for search-ready summaries
