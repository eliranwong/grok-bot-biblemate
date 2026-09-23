---
name: Chronology
description: "Expound biblical chronology using local datasets and academic-historical knowledge. Use when the user runs /chronology or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/chronology
---
# Chronology

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
# Chronology Skill

## Overview
This standalone skill enables any agent to search and expound biblical, royal, and apostolic timelines. It queries a set of local chronology text files to locate matching records, and complements those findings with historical-grammatical scholarship.

## Guidelines & Objectives
When executing this skill:
- Always run the python script located at `/home/box/agent-data/biblemate-native-skills/chronology/chronology_query.py` to search the local timeline databases.
- Execute the script using: `python3 /home/box/agent-data/biblemate-native-skills/chronology/chronology_query.py "<query>"` where `<query>` is the input prompt, a specific year, name, or event.
- If relevant matching records are found in the local text files, display them with clear headings referencing their source file.
- If the requested chronological information is not found in the dataset, or is incomplete, use your own extensive biblical and historical knowledge to answer, clearly stating that the explanation is augmented by general academic/scholarly knowledge.

## Slash command guidance

Folded from the Grok Build command `/chronology` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** (for Old Testament periods), **NT Bible Scholar** (for New Testament periods), or **Biblical Theologian** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md` depending on the context of the query.

Use the **chronology** skill to search the local database for historical matches.

Please search the local chronology database and expound the timeline based on the following input. If the requested information is not found in the dataset, you must answer using your own extensive scholarly and historical knowledge of the scriptures:

# Input

user arguments after the slash command

