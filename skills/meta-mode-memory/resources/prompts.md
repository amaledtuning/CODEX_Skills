# Prompt Templates

## Reflection Capture

```text
Title: <short title>
Kind: reflection
Tags: <tag1>, <tag2>
Body:
- Stable compact facts (never full history)
- Stable facts and assumptions
- Decisions made
- Do-not-reask decisions
- What was blocked and why
- Validation performed
- Changed files
- Next steps
```

## Session Capture

```text
Title: <session name>
Kind: session
Tags: <feature>, <context>
Body:
- Keep markdown body short and query-friendly
- Goal
- Stable facts
- Actions taken
- Decisions
- Do-not-reask decisions
- Blockers
- Validation
- Changed files
- Next steps
```

## Decision Record

```text
Title: <decision title>
Kind: decision
Tags: <domain>, <tradeoff>
Body:
- Decision
- Do-not-reask decision, if the user has settled it
- Alternatives considered
- Tradeoffs
- Impact on existing work
- Validation checks
- Follow-up next steps
```

## Compact State Payload

```text
State payload (JSON):
{
  "task_id": "task-uuid",
  "title": "short task title",
  "updated_at": "ISO-8601 timestamp",
  "status": "in_progress|blocked|complete",
  "tags": ["tag1", "tag2"],
  "facts": ["fact_1", "fact_2"],
  "decisions": ["decision_1"],
  "do_not_reask_decisions": ["settled decision not to re-ask unless new evidence appears"],
  "blockers": ["blocker_1"],
  "sources": ["daily/YYYY-MM-DD.md"],
  "changed_files": ["path/to/file1", "path/to/file2"],
  "validation": ["sanity check names"],
  "next_steps": ["next action"]
}
```

## Forbidden content in prompts

- Never include:
  - raw chat transcripts
  - full source files
  - raw logs
  - long diffs
  - credentials, tokens, secrets

## Language Policy

- Internal worker outputs are English unless explicitly user-facing in another language.
- User-facing language follows the active policy stack for the current session.

## Query Output Style

```text
Return top matches as:
1) relevance score
2) file path
3) concise snippet (1-2 lines)
4) optional next file to inspect
```

