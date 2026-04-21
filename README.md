# CODEX Skills Publish Artifact

This staging bundle prepares selected self-authored Codex skills for publishing to the `amaledtuning/CODEX_Skills` repository.

## Included Skills

- `universal-orchestrator-rules`
- `parallel-task-decomposition`
- `active-session-continuity`
- `chat-handoff-checkpoint`
- `meta-mode-memory`
- `parallel-codex-execution`

## Layout

- `skills/<skill-name>/...`

## Installation / Copy

1. Copy one or more skill folders from `skills/` into your Codex skills directory.
2. Typical target is `~/.codex/skills/<skill-name>`.
3. Restart or refresh your Codex session so runtime skill discovery can pick up copied skills.

## Safety Notes

- This artifact excludes generated caches and temporary files.
- Memory data must not be published; `.agents/memory` is excluded.
- Review contents before pushing to any remote repository.

## Routing Notes

- Cheap read-only route: `agent_type=default` + `gpt-5.4-mini` + `reasoning_effort=medium`.
- Ordinary implementation route: `gpt-5.3-codex` + `reasoning_effort=medium`.
- Route metadata is diagnostic only.
