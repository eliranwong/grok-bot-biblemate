---
name: Questions
description: "Create engaging, small-group discussion questions based on a bible passage. Use when the user runs /questions or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/questions
---
# Questions

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
# Questions Skill

## Overview
This standalone skill enables any agent to perform a high-quality questions study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Create engaging, small-group discussion questions based on a passage. Provide three tiers:
1. **Observation Questions**: Helping readers see exactly what the text says (literary features, grammar, facts).
2. **Interpretation Questions**: Helping readers understand what the text means (themes, theology, cultural context).
3. **Application Questions**: Helping readers apply the text to their personal lives, relationships, and spiritual growth.

## Slash command guidance

Folded from the Grok Build command `/questions` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Compassionate Pastor** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Assist me to prepare materials for leading a bible study group.
I'm looking for specific questions that focus on a particular passage, rather than general bible study questions. Could you help me with that?
I'm hoping to facilitate a meaningful discussion and deeper understanding of this passage through targeted questions. Could you guide me in creating those questions?
Remember, I am already familiar with the contents of the passage, please refrain from providing me with general information or summary. Please give me review questions for bible studies directly.

Please answer all relevant questions pertaining to the following passage:

# Passage

user arguments after the slash command

