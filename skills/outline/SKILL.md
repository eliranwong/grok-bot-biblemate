---
name: Outline
description: "Generate a detailed, structural outline of a bible book or passage down to small sections. Use when the user runs /outline or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/outline
---
# Outline

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
# Outline Skill

## Overview
This standalone skill enables any agent to perform a high-quality outline study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Generate a detailed structural outline of a bible book or passage down to small sections. For each unit:
1. **Segment Divisions**: Mark the starting and ending verses for each subsection.
2. **Descriptive Title**: Provide a concise, thematic title for each section.
3. **Structural and Literary Notes**: Note structural devices (e.g., inclusio, chiasms, shifts in speaker, or genre changes) that justify the division.

## Slash command guidance

Folded from the Grok Build command `/outline` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** (for Old Testament books/passages) or **NT Bible Scholar** (for New Testament books/passages) persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

I am currently studying the following bible book and chapters and would appreciate it if you could provide me with a detailed outline for it.
I want an outline for all chapters of the bible book and chapters I am giving you.
Please divide it into several main sections and under each section, divide it into different passages.
Break down the passages into the smallest ones possible, as I am looking for a highly detailed outline.
Additionally, kindly provide a title for each passage.
Remember, use your own analysis based on the bible text instead of copying a published outline.
If chapters are not specified, provide an outline to cover all chapters of the bible book given.

# Bible reference

user arguments after the slash command

