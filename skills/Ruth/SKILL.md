---
name: Ruth
description: "Search for given words or phrases in the book of Ruth in one or multiple bibles, with wildcards (*, ?) and logical combinations (+, |) supported. Use when the user runs /Ruth or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/Ruth
---
# Ruth

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
# Bible Search Skill - Ruth

## Overview
This standalone skill enables any agent to search for words or phrases inside the book of Ruth in local SQLite Bible databases stored in `/workspace/biblemate/data/bibles` or `/workspace/biblemate/data_custom/bibles`.

## Guidelines & Objectives
When executing this skill:
- Always run the python retriever script located at `/home/box/agent-data/biblemate-native-skills/search/search_retriever.py` with the `--book Ruth` option to perform the search.
- Execute the script using: `python3 /home/box/agent-data/biblemate-native-skills/search/search_retriever.py --book Ruth "<query>"` where `<query>` is the input prompt or arguments.
- Pass the user's version and search query exactly as given to the script.
- Present the exact output of the script to the user without summarizing, paraphrasing, or altering the text, maintaining the absolute authority and accuracy of God's Word.

## Slash command guidance

Folded from the Grok Build command `/Ruth` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Verse Scripter** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **Ruth** skill to search for words or phrases in the book of Ruth.

Please search the book of Ruth and retrieve matching verses based on the following input:

# Input

user arguments after the slash command

