---
name: Sync
description: "Git add, commit, and push all latest changes to the remote repository. Use when the user runs /sync or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/sync
---
# Sync

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
# Sync Skill

## Overview
This standalone skill enables the agent to stage, commit, and push all latest workspace changes to the remote Git repository.

## Guidelines & Objectives
When executing this skill:
1. **Analyze Workspace State**: Run a check on the repository using `git status` to see what files have been modified, created, or deleted.
2. **Stage Changes**: Run `git add .` to stage all changes in the current workspace.
3. **Commit Changes**: Create a descriptive commit message that summarizes the main updates. If the user provided a custom commit message (e.g., via the slash command argument), use that message. Otherwise, construct a clean message (e.g., "Sync latest changes" or a list of modified files) and run `git commit -m "<commit_message>"`.
4. **Push to Remote**: Run `git push` to upload the changes to the remote repository.
5. **Verify and Report**: Confirm that the push succeeded and present a clean summary of the synced changes to the user.

## Slash command guidance

Folded from the Grok Build command `/sync` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Verse Scripter** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **sync** skill to stage, commit, and push all latest changes in the workspace to the remote repository.

Please perform the git sync. If a commit message is provided as input, use it as the commit message. Otherwise, generate a descriptive commit message based on the modified files, or default to a message like "Sync latest changes".

# Input

user arguments after the slash command

