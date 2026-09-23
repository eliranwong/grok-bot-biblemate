---
name: BibleMate Studies CLI
description: "Use when the user asks to run a Bible study, devotion, sermon prep, slash command, or any query against the BibleMate agentic workspace — prefer native Grok Bot skills, else grok/claude/agy CLIs as fallback. Use when the user runs /biblemate-studies-cli."
ecosystem: biblemate
port: grok-bot-native
---
# BibleMate Studies CLI

Prefer **native** Grok Bot BibleMate playbooks. Fall back to the agentic workspace CLIs (`grok` / `claude` / `agy`) when the user asks for the CLI path, a native skill is missing/broken, or you need the Grok Build `.grok` surface.

## Defaults

| Mode | Working directory | When |
|------|-------------------|------|
| **Native (preferred)** | Playbooks in `/home/box/agent-data/biblemate-native-skills/`; reports under `/workspace/grok-bot-biblemate/` | Known slash commands (`/bible`, `/devotion`, `/sermon`, `/biblemate`, `/Gen`, …) |
| **CLI fallback** | `/workspace/biblemate-agentic-workspace` (must contain `.grok/`) or `/workspace/biblemate_studies` | User asks for CLI, native path unavailable, or Build-only workflow |

### CLI flags (pre-cleared for this ecosystem)

- Primary: `grok --always-approve -p "<query>"`
- If asked or grok fails: `claude -p "<query>"`
- Last resort: `agy --dangerously-skip-permissions -p "<query>"`
- Do **not** re-ask for per-step approval on routine studies/devotions/sermons.
- Only confirm first if the query is clearly destructive (wipe, reset, force-push, mass delete).

## Steps (native path)

1. Match the ask to a catalog / playbook id (e.g. `devotion`, `sermon`, `bible`, `Gen`).
2. Read `/home/box/agent-data/biblemate-native-skills/<id>/SKILL.md` and execute with Grok Bot tools (`WebSearch`, `WebFetch`, `Read`, `Shell`, `Task`/executor).
3. Never invent Scripture — fetch via `bible` / `bible_retriever.py`. Defaults when unspecified: **CSB** (English), **CUV** (Chinese).
4. Write the **full, uncompromised report** under `/workspace/grok-bot-biblemate/` in the folder the playbook names (`biblemate/`, `devotions/`, `sermons/`, `studies/`).
5. `SendToUser` a short pastoral digest **and** a chat copy of the report (paste or attach the `.md`) plus the concrete path.

## Steps (CLI fallback)

1. Prefer `/workspace/biblemate-agentic-workspace/.grok` if present; else `/workspace/biblemate_studies`. If neither exists, tell the user — do not invent a CLI run against the Bot-only repo.
2. `cd` into the chosen Build/studies repo.
3. Translate the ask into a clear `-p` query (keep slash forms like `/bible`, `/sermon`, `/devotion`, `/biblemate`, `/Gen`).
4. Quote safely (HEREDOC or carefully escaped quotes).
5. Run with a long enough timeout; background if needed; notify when finished.
6. Inspect new/changed report files under `biblemate/` (or the repo's study output folders).
7. `SendToUser` a short pastoral digest **and** a chat copy (or attach the main `.md`) plus concrete paths.

## Notes

- Native skills and CLI fallback are complementary: native = Grok Bot tools + this Bot repo; CLI = Grok Build package in `biblemate-agentic-workspace` / `biblemate_studies`.
- One CLI per request unless the user asked to compare tools.
- Repo sync for **this** Bot pack: `/gbm-ecosystem-sync`. Build repo sync: that ecosystem's own `/sync`.

