---
name: Names
description: "Retrieve and compare the meanings of names in the Bible. Use when the user runs /names or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/names
---
# Names

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
# Names Skill

## Overview
This standalone skill enables any agent to search and expound the etymological and spiritual meanings of biblical names. It queries a local database of Bible names and their associated meanings, supporting spelling flexibility for misspelled queries.

## Guidelines & Objectives
When executing this skill:
- Always run the python script located at `/home/box/agent-data/biblemate-native-skills/names/names_query.py` to search the local name definitions database.
- Execute the script using: `python3 /home/box/agent-data/biblemate-native-skills/names/names_query.py "<query>"` where `<query>` is the name or search terms.
- If relevant matching records are found in the local database, display them clearly.
- If the requested name is not found in the dataset, or you wish to elaborate, use your own extensive linguistic and biblical knowledge (including Hebrew/Greek roots and historical significance) to answer, clearly stating that the information is augmented by general biblical-linguistic knowledge.

## Slash command guidance

Folded from the Grok Build command `/names` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Biblical Linguistic Analyst** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **names** skill to search the local database for name meanings.

Please search the local database and expound the meaning of the requested Bible name based on the following input. If the name is not found in the dataset, you must answer using your own extensive scholarly, historical, and linguistic knowledge of the scriptures:

# Input

user arguments after the slash command

