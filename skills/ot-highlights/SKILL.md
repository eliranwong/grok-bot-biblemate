---
name: OT Highlights
description: "Outline key highlights, major events, and summaries for an Old Testament passage. Use when the user runs /ot-highlights or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/ot-highlights
---
# OT Highlights

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
# Ot Highlights Skill

## Overview
This standalone skill enables any agent to perform a high-quality ot highlights study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Outline key highlights, major events, and summaries for an Old Testament passage:
1. **Narrative/Theological Milestones**: Pivotal events, miracles, speeches, or commands.
2. **Covenantal Signs**: How this passage updates, enforces, or fulfills God's covenant promises.
3. **Major Disclosures**: Core revelations about God's character, judgment, or salvation.

## Slash command guidance

Folded from the Grok Build command `/ot-highlights` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Bible Highlights in an Old Testament passage in the bible.
Can you give me a detailed summary of this passage?
How can the meaning of the biblical Hebrew words in this passage provide insights that aid our understanding? Explain the insights with examples.
What are the key words and phrases used in this passage, and how do they contribute to its meaning?
How does this passage relate to other passages in the Bible, both within the same book and in other books?
Please answer all relevant questions pertaining to the following passage.
You don't need to provide all the verses from the passage, as I am already familiar with it. 
I want your response focus on my questions.  However, do not repeat my questions word by word in your answer.

Please write in detail pertaining to the following passage:

# Passage

user arguments after the slash command

