---
name: ZIP
description: "Create manual_setup.zip containing .grok/, preferences/, and AGENTS.md for manual Grok Build repository setup. Use when the user runs /zip or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/zip
---
# ZIP

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
# Zip Archive Skill (Grok Bot)

## Overview
This skill packages the `.grok/` configuration, root `preferences/`, and root
`AGENTS.md` into a single `manual_setup.zip` at the repository root. That
archive lets users manually import the Grok Bot BibleMate personas, skills,
slash commands, and database preferences into a new repository.

## Guidelines & Objectives
When executing this skill:
1. **Remove Existing Archive**: Before creating a new zip file, always check for
   the existence of `manual_setup.zip` in the root of the repository. If it
   exists, delete it first to ensure the archive is built fresh.
2. **Execute Python Helper**: Run the zip creator script:
   ```bash
   python3 /home/box/agent-data/biblemate-native-skills/zip/zip_creator.py
   ```
3. **Git Integration**: The script will automatically detect if the repository
   is a Git repository. If it is, and `manual_setup.zip` has modifications, it
   will stage, commit, and push it to the remote repository.
4. **Report Status**: Once the ZIP archive is successfully created and Git
   integration has run, output a clear summary confirming the creation of
   `manual_setup.zip` and the Git synchronization status.

## Slash command guidance

Folded from the Grok Build command `/zip` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Verse Scripter** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **zip** skill to create a zip file in the root of this repository, naming it as `manual_setup.zip`, to zip the `.grok/`, `preferences/` folders, and the `AGENTS.md` and `CLAUDE.md` files.

