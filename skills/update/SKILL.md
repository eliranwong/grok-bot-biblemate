---
name: Update
description: "Refresh the BibleMate Grok Build ecosystem by re-running the local generator against the latest Claude Code (or antigravity) source. Use when the user runs /update or asks to regenerate the .grok ecosystem."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/update
---
# Update

## Grok Bot runtime notes (native port)

This skill was ported from the BibleMate Grok Build `.grok` playbook for **native Grok Bot** execution.

### Tool mapping
| Playbook concept | Use on Grok Bot |
|------------------|-----------------|
| Web research | `WebSearch`, `WebFetch` |
| Read files | `Read` |
| Shell / scripts | `Shell` (`python3` on helpers beside this playbook under `/home/box/agent-data/biblemate-native-skills/`) |
| Parallel workers | `Task` with `subagent_type: executor` (or MessageSubagent to steer) |
| Save reports | Write the **full, uncompromised** report under `/workspace/grok-bot-biblemate/` in the folders the playbook names (`biblemate/`, `devotions/`, `sermons/`, `studies/`, …) |
| User-visible result | Always `SendToUser` a short digest **and** a chat copy of the report (paste full text or attach the saved `.md`) + concrete path when finished |

### Rules
- Do **not** shell out to `grok`/`claude`/`agy` for this skill — execute the methodology yourself with the tools above.
- **Never invent Scripture text.** Fetch verses via the `bible` skill / `bible_retriever.py` (local SQLite under `/workspace/biblemate/data/bibles` and `/workspace/biblemate/data_custom/bibles`; also mirrored at `/home/box/biblemate/...`).
- Default translations when unspecified: **CSB** (English), **CUV** (Chinese). Prefer Cantonese (粵語) for devotionals/check-ins when the user's language preference suggests it.
- Adopt a warm pastoral tone (Compassionate Pastor / related personas from BibleMate agents.md) unless the skill names a different persona.
- Prefer parallel tool calls where the playbook says to run work together.
- Working directory for artifacts: `/workspace/grok-bot-biblemate` (report folders sync to git — do not treat as disposable cache).
- On every finished run: full report on disk **and** chat copy via `SendToUser` (attach `.md` for long reports).
- When the playbook mentions sibling skills, read the full playbook under `/home/box/agent-data/biblemate-native-skills/<id>/SKILL.md` (catalog loaders under `/home/box/agent-data/workflows/` point there after install).
- Helper scripts live beside the playbook after install, e.g. `python3 /home/box/agent-data/biblemate-native-skills/bible/bible_retriever.py "<query>"`.

---
# Update Skill (Grok Bot)

## Overview
This skill refreshes the self-contained `.grok` BibleMate ecosystem for Grok
Build. Preferred path when `.claude/` is already present: regenerate directly
from Claude Code sources. Optional path: download the remote `manual_setup.zip`
bundle first (ships `.agents/` + `preferences/`), rebuild Claude via
`python3 .claude/build_claude.py` if available, then rebuild Grok.

Everything this skill needs for the Grok rebuild lives inside `.grok/` (this
generator) plus the `.claude/` tree as source.

## Guidelines & Objectives
1. **Verify Operating System**: Only supported on macOS or Linux.
2. **Verify Workspace Folder**: Prefer not to run destructive updates inside a
   workspace named `antigravity-biblemate-workspace` (the source repository)
   unless you intentionally maintain this repo. Confirm with the user first.
3. **Optional download & extract** (if `.claude/` is missing or stale and the
   user wants a remote refresh):
   ```bash
   python3 /home/box/agent-data/biblemate-native-skills/update/updater.py
   ```
   If the Claude updater exists, you may also run:
   ```bash
   python3 .claude/skills/update/updater.py
   python3 .claude/build_claude.py
   ```
4. **Regenerate `.grok`**: Rebuild the Grok Bot ecosystem from `.claude/`:
   ```bash
   python3 /workspace/biblemate-agentic-workspace/.grok/build_grok.py
   ```
5. **Report Status**: Summarise whether regeneration succeeded, and list the
   number of skills/commands/agents/personas regenerated.

## Slash command guidance

Folded from the Grok Build command `/update` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Verse Scripter** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **update** skill to verify conditions (OS and workspace name) and run the update command to initialize workspace directories.

